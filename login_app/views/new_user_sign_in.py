import uuid

from django.views.generic import FormView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from login_app.forms import ContactEmailForm

from identity_models.user_details import UserDetails


class NewUserSignInFormView(FormView):
    """
    Class containing the methods for handling requests to the 'New-User-Sign-In' page.
    """
    template_name = 'new-user-sign-in.html'
    form_class = ContactEmailForm
    success_url = 'Check-New-Email'

    def form_valid(self, request):
        email_address = request.cleaned_data['email_address']
        record = UserDetails.api.get_record(email=email_address)

        if record.status_code == 404:
            UserDetails.api.create(email=email_address, application_id=uuid.uuid4())

        # TODO - Add calls to Notify-Gateway API to send email to appplicant, once above implemented.

        return HttpResponseRedirect(reverse(self.success_url))
