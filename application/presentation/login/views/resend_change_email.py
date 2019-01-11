from django.shortcuts import render
from django.views import View
from django.conf import settings

from application.services import notify
from application.presentation import utilities

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions

from .change_email import send_change_email_email


class ResendChangeEmail(View):
    """
    Class containing the methods for handling requests to the 'Resend-Email' page.
    """
    def get(self, request):
        email_address = request.GET['email_address']
        application_id = request.GET['id']

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

        # Get first_name if it exists, otherwise use 'Applicant'
        if personal_details_record_exists:
            first_name = personal_details_response.record['first_name']
        else:
            first_name = "Applicant"

        # Check if email already exists/in use
        existing_account_response = identity_actions.list('user', params={'email': email_address})
        existing_account_response_status_code = existing_account_response.status_code

        email_in_use = existing_account_response_status_code == 200

        if email_in_use:
            if settings.DEBUG:
                print("You will not see an email validation link printed because an account already exists with that email.")
        else:
            # Generate a new magic link and expiry date
            validation_link, email_expiry_date = utilities.generate_email_validation_link(email_address)
            magic_link = validation_link.split('/')[-1]
            validation_link += '?email=' + email_address

            # Create an update record with the magic_link information
            email_update_record = user_identity_record
            email_update_record['magic_link_email'] = magic_link
            email_update_record['email_expiry_date'] = email_expiry_date

            # Update the user record
            IdentityGatewayActions().put('user', params=email_update_record)

            # Send the 'Change Email' email
            if settings.DEBUG:
                print(validation_link)

            send_change_email_email(email_address, first_name, validation_link)

        return render(request, template_name='email-resent.html', context={'id': application_id,
                                                                           'email_address': email_address})
