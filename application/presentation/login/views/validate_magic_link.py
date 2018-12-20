import time

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.views import View
from nanny import notify
from nanny import utilities
from nanny.middleware import CustomAuthenticationHandler
from nanny.db_gateways import IdentityGatewayActions


class ValidateMagicLinkView(View):
    record = None

    def get(self, request, id):
        identity_actions = IdentityGatewayActions()
        api_response = identity_actions.list('user', params={'magic_link_email': id})

        if api_response.status_code == 200:

            self.record = api_response.record[0]

            if not self.link_has_expired():

                # If user has come from the 'Change Email' journey
                if 'email' in request.GET:
                    # Update the user's email
                    new_email = request.GET.get('email')
                    new_email_record = self.record
                    new_email_record['email'] = new_email

                    response = identity_actions.put('user', params=new_email_record)

                    if response.status_code != 200:
                        return HttpResponseRedirect(reverse('Service-Unavailable'))

                    http_response = HttpResponseRedirect(self.get_success_url())
                    CustomAuthenticationHandler.create_session(http_response, new_email)
                    return http_response

                return HttpResponseRedirect(self.get_success_url())

            else:
                return HttpResponseRedirect(reverse('Link-Used'))

        elif api_response.status_code == 404:
            return HttpResponseRedirect(reverse('Link-Used'))

        else:
            return HttpResponseRedirect(reverse('Service-Unavailable'))

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

        elif 'email' in self.request.GET:
            success_template = 'Task-List'

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

        notify.send_text(
            record['mobile_number'],
            personalisation={'link': magic_link_sms},
            template_id='1c3f0e2f-d9df-474e-9649-db262c9a8dbc'
        )

        return record