from django.views.generic import TemplateView

import uuid

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from nanny import notify
from login_app.forms import ContactEmailForm
from nanny import utilities
from .base import BaseFormView

from nanny.db_gateways import IdentityGatewayActions


class ChangeEmailTemplateView(BaseFormView):
    """
    View for handling requests to 'Change-Email' page.
    """
    template_name = 'change-email.html'
    form_class = ContactEmailForm
    success_url = 'Check-New-Email'
    email_address = None

    def form_valid(self, form):
        if not utilities.test_notify():
            return HttpResponseRedirect(reverse('Service-Unavailable'))

        application_id = self.request.GET.get('id')
        self.email_address = form.cleaned_data['email_address']

        identity_actions = IdentityGatewayActions()
        user_identity_record = identity_actions.read('user',
                                                     params={'application_id': application_id}).record

        account_email = user_identity_record['email']

        existing_account_response = identity_actions.list('user', params={'email': self.email_address})
        existing_account_response_status_code = existing_account_response.status_code

        email_in_use = existing_account_response_status_code == 200

        if self.email_address == account_email:
            # If email is unchanged, return to the sign-in details check-answers page
            return HttpResponseRedirect(reverse('Placeholder') + '?id=' + application_id)

        elif email_in_use:
            # If the email is already being used,
            if settings.DEBUG:
                print(
                    "You will not see an email validation link printed because an account already exists with that email.")
            return HttpResponseRedirect(reverse('Placeholder') + '?email=' + self.email_address)

        else:
            # TODO: Send update email, redirect to page.
            pass
            # # Send an email to the new email adddress, with the account's ID in the link.
            # update_magic_link(email, app_id)
            # redirect_url = build_url('Update-Email-Sent', get={'email': email, 'id': app_id})
            # return HttpResponseRedirect(redirect_url)

        # return HttpResponseRedirect(self.get_success_url())
