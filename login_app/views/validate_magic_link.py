import time

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import reverse

from identity_models.user_details import UserDetails

from nanny import notify
from nanny import utilities


class ValidateMagicLinkView(View):
    def get(self, request, id):
        api_response = UserDetails.api.get_record(magic_link_email=id)
        self.record = api_response.record

        if not self.link_has_expired() and api_response.status_code == 200:
            return HttpResponseRedirect(self.get_success_url())

        else:
            return HttpResponseRedirect(reverse('Link-Used'))

    def link_has_expired(self):
        # Expiry period is set in hours in settings.py
        exp_period = settings.EMAIL_EXPIRY * 60 * 60
        diff = int(time.time() - self.record['email_expiry_date'])
        if diff < exp_period or diff == exp_period:
            return False
        else:
            return True

    def get_success_url(self):
        if not len(self.record['mobile_number']):
            success_template = 'Phone-Number'

        else:
            self.record = self.sms_magic_link(self.record)
            success_template = 'Security-Code'

        self.record['email_expiry_date'] = 0
        UserDetails.api.put(self.record)
        return utilities.build_url(success_template, get={'id': self.record['application_id']})

    @staticmethod
    def sms_magic_link(record):
        magic_link_sms, sms_expiry_date = utilities.generate_sms_code()

        record['magic_link_sms'] = magic_link_sms
        record['sms_expiry_date'] = sms_expiry_date

        notify.send_text(record['mobile_number'],
                         personalisation={'link': magic_link_sms},
                         template_id='d285f17b-8534-4110-ba6c-e7e788eeafb2')

        return record
