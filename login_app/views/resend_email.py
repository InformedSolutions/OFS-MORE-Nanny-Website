from django.shortcuts import render
from django.views import View

from nanny import notify, utilities

from nanny.db_gateways import IdentityGatewayActions


class ResendEmail(View):
    """
    Class containing the methods for handling requests to the 'Resend-Email' page.
    """
    def get(self, request):
        email_address = request.GET['email_address']
        api_response = IdentityGatewayActions().list('user', params={'email': email_address})
        record = api_response.record[0]
        validation_link, email_expiry_date = utilities.generate_email_validation_link(email_address)

        record['magic_link_email'] = validation_link.split('/')[-1]
        record['email_expiry_date'] = email_expiry_date
        IdentityGatewayActions().put('user', params=record)

        # Set Nanny email template
        # If existing user
        if record['mobile_number'] != '':
            template_id = '5d983266-7efa-4978-9d4c-9099ed6ece28'
        # If new user
        else:
            template_id = '45c6b63e-1973-45e5-99d7-25f2877bebd9'

        # Send a Nanny email
        notify.send_email(email=email_address,
                          personalisation={"link": validation_link},
                          template_id=template_id)

        return render(request, template_name='email-resent.html', context={'email_address': email_address})
