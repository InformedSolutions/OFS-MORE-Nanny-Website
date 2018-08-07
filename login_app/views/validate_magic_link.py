import time

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import reverse

from nanny import notify
from nanny import utilities

from nanny.db_gateways import IdentityGatewayActions


class ValidateMagicLinkView(View):
    def get(self, request, id):
        api_response = IdentityGatewayActions().list('user', params={'magic_link_email': id})
        self.record = api_response.record[0]

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
        IdentityGatewayActions().put('user', params=self.record)
        return utilities.build_url(success_template, get={'id': self.record['application_id']})

    @staticmethod
    def sms_magic_link(record):
        magic_link_sms, sms_expiry_date = utilities.generate_sms_code()

        record['magic_link_sms'] = magic_link_sms
        record['sms_expiry_date'] = sms_expiry_date

        notify.send_text(record['mobile_number'],
                         personalisation={'link': magic_link_sms},
                         template_id='6947f254-5033-41b6-8fc5-5fcc6d613b66')

        return record
