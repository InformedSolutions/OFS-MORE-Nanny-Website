import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from application.services import notify
from ..forms import ContactEmailForm
from application.presentation import utilities
from .base import BaseFormView

from application.services.db_gateways import IdentityGatewayActions


class NewUserSignInFormView(BaseFormView):
    """
    Class containing the methods for handling requests to the 'New-User-Sign-In' page.
    """
    template_name = 'new-user-sign-in.html'
    form_class = ContactEmailForm
    success_url = 'Check-New-Email'
    email_address = None

    def form_valid(self, email_form):
        if not utilities.test_notify():
            return HttpResponseRedirect(reverse('Service-Unavailable'))

        email_address = email_form.cleaned_data['email_address']
        self.email_address = email_address  # Set such that success parameters can find value later.
        api_response = IdentityGatewayActions().list('user', params={'email': email_address, 'service': "NANNY"})

        if api_response.status_code == 404:
            api_response = IdentityGatewayActions().create('user', {'email': email_address, 'application_id': uuid.uuid4(), 'service': "NANNY"})
            record = api_response.record
        else:
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

        # Send Nanny email
        notify.send_email(email=email_address,
                          personalisation={"link": validation_link},
                          template_id=template_id)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_parameters(self):
        return {'email_address': self.email_address}
