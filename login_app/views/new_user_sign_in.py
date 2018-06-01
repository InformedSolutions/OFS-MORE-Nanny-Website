from django.views.generic import FormView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from login_app.forms import ContactEmailForm


class NewUserSignInFormView(FormView):
    """
    Class containing the methods for handling requests to the 'New-User-Sign-In' page.
    """
    template_name = 'new-user-sign-in.html'
    form_class = ContactEmailForm
    success_url = 'Service-Unavailable'

    def form_valid(self, request):
        #TODO - Insert calls to Identity-Gateway API for creation of new application.

        # return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse(self.success_url))
