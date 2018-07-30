from django.shortcuts import render
from django.views import View

from nanny import notify, utilities

from db_gateways import IdentityGatewayActions


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

        # Send an example email from the CM application login journey.
        notify.send_email(email=email_address,
                          personalisation={"link": validation_link},
                          template_id='45c6b63e-1973-45e5-99d7-25f2877bebd9')

        return render(request, template_name='email-resent.html', context={'email_address': email_address})
