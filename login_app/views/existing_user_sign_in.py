from django.views.generic import FormView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from login_app.forms import ContactEmailForm


class ExistingUserSignInFormView(FormView):
    """
    Class containing the methods for handling requests to the 'New-User-Sign-In' page.
    """
    template_name = 'existing-user-sign-in.html'
    form_class = ContactEmailForm
    success_url = 'Check-Existing-Email'

    def form_valid(self, request):
        # TODO - Insert calls to Identity-Gateway API for creation of new application.
        # TODO - Add calls to Notify-Gateway API to send email to appplicant, once above implemented.

        # return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse(self.success_url))
