import uuid

from django.http import HttpResponseRedirect

from identity_models.user_details import UserDetails

from login_app import notify
from login_app.forms import ContactEmailForm
from login_app import utils
from .base import BaseFormView


class NewUserSignInFormView(BaseFormView):
    """
    Class containing the methods for handling requests to the 'New-User-Sign-In' page.
    """
    template_name = 'new-user-sign-in.html'
    form_class = ContactEmailForm
    success_url = 'Check-New-Email'

    def form_valid(self, email_form):
        email_address = email_form.cleaned_data['email_address']
        api_response = UserDetails.api.get_record(email=email_address)

        if api_response.status_code == 404:
            UserDetails.api.create(email=email_address, application_id=uuid.uuid4())

        record = api_response.record
        validation_link, email_expiry_date = utils.generate_email_validation_link(email_address)

        record['magic_link_email'] = validation_link.split('/')[-1]
        record['email_expiry_date'] = email_expiry_date
        UserDetails.api.put(record)

        # Send an example email from the CM application login journey.
        notify.send_email(email=email_address,
                          personalisation={"link": validation_link},
                          template_id='ecd2a788-257b-4bb9-8784-5aed82bcbb92')

        return HttpResponseRedirect(self.get_success_url())
