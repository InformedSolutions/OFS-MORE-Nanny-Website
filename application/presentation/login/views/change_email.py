from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from application.services import notify
from ..forms import ContactEmailForm
from application.presentation import utilities
from .base import BaseFormView

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


class ChangeEmailTemplateView(BaseFormView):
    """
    View for handling requests to 'Change-Email' page.
    """
    template_name = 'change-email.html'
    form_class = ContactEmailForm
    check_answers_url = 'Contact-Details-Summary'
    success_url = 'Check-Change-Email'
    email_address = None

    def get_context_data(self, **kwargs):
        context = super(ChangeEmailTemplateView, self).get_context_data(**kwargs)
        context['id'] = self.request.GET.get('id')
        context['change_email'] = self.request.GET.get('change_email')
        return context

    def form_valid(self, form):
        if not utilities.test_notify():
            return HttpResponseRedirect(reverse('Service-Unavailable'))

        application_id = self.request.GET.get('id')
        self.email_address = form.cleaned_data['email_address']

        # Create GatewayActions instances
        identity_actions = IdentityGatewayActions()
        nanny_actions = NannyGatewayActions()

        # Get relevant records
        user_identity_record = identity_actions.read('user',
                                                     params={'application_id': application_id}).record

        # Get personal_details response, not record, and check if a record exists
        personal_details_response = nanny_actions.read('applicant-personal-details',
                                                     params={'application_id': application_id})
        try:
            personal_details_record_exists = personal_details_response.record is not None
        except AttributeError:
            personal_details_record_exists = False

        # Get user's current email
        account_email = user_identity_record['email']

        # Get first_name if it exists, otherwise use 'Applicant'
        if personal_details_record_exists:
            first_name = personal_details_response.record['first_name']
        else:
            first_name = "Applicant"

        existing_account_response = identity_actions.list('user', params={'email': self.email_address})
        existing_account_response_status_code = existing_account_response.status_code

        email_in_use = existing_account_response_status_code == 200

        if self.email_address == account_email:
            # If email is unchanged, return to the sign-in details check-answers page
            same_email_redirect = utilities.build_url(self.check_answers_url,
                                                          get={'id': application_id})
            return HttpResponseRedirect(same_email_redirect)

        elif email_in_use:
            # If the email is already being used,
            if settings.DEBUG:
                print("You will not see an email validation link printed because an account already exists with that email.")
            not_sent_email_redirect = utilities.build_url(self.success_url,
                                                      get={'id': application_id})
            email_address = self.email_address
            return HttpResponseRedirect(not_sent_email_redirect)

        else:
            change_email = self.email_address
            # Generate a new magic link and expiry date
            validation_link, email_expiry_date = utilities.generate_email_validation_link(change_email)
            magic_link = validation_link.split('/')[-1]

            # Create an update record with the magic_link information
            email_update_record = user_identity_record
            email_update_record['magic_link_email'] = magic_link
            email_update_record['email_expiry_date'] = email_expiry_date
            email_update_record['change_email'] = change_email

            # Update the user record
            record = IdentityGatewayActions().put('user', params=email_update_record)

            # Send the 'Change Email' email
            if settings.DEBUG:
                print(validation_link)

            send_change_email_email(change_email, first_name, validation_link)

            sent_email_redirect = utilities.build_url(self.success_url, get={'id': application_id})

            return HttpResponseRedirect(sent_email_redirect)

def send_change_email_email(email, first_name, url):
    """
    Method to send a 'Change Email' email using the Notify Gateway API
    :param email: string containing the e-mail address to send the e-mail to
    :param first_name: string first name
    :param magic_link: url directing to email validation page.
    :return: HTTP response
    """
    if hasattr(settings, 'NOTIFY_URL'):
        email = str(email)
        template_id = '108ecfa0-4496-4ce7-97c8-f43c9f42a374'
        personalisation = {'first_name': first_name, 'magic_link': url}
        return notify.send_email(email, personalisation, template_id)

