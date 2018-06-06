import uuid

from django.http import HttpResponseRedirect

from identity_models.user_details import UserDetails

from login_app.forms import ContactEmailForm
from .base import BaseFormView


class ExistingUserSignInFormView(BaseFormView):
    """
    Class containing the methods for handling requests to the 'New-User-Sign-In' page.
    """
    template_name = 'existing-user-sign-in.html'
    form_class = ContactEmailForm
    success_url = 'Check-Existing-Email'

    def form_valid(self, email_form):
        email_address = email_form.cleaned_data['email_address']
        record = UserDetails.api.get_record(email=email_address)

        if record.status_code == 404:
            UserDetails.api.create(email=email_address, application_id=uuid.uuid4())

        # TODO - Add calls to Notify-Gateway API to send email to applicant.

        return HttpResponseRedirect(self.get_success_url())

    def get_success_parameters(self):
        """
        Method to return a dictionary of parameters to be included as variables in the success url, e.g. application_id.
        """
        params = dict()
        params['email_address'] = self.request.POST['email_address']

        return params
