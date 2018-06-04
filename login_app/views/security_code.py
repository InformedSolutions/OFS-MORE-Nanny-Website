from django.views.generic import FormView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from login_app.forms import SecurityCodeForm


class SecurityCodeFormView(FormView):
    """
    Class containing the methods for handling requests to the 'Security-Code' page.
    """
    template_name = 'security-code.html'
    form_class = SecurityCodeForm
    success_url = 'Security-Code'

    def form_valid(self, request):
        # TODO - Add calls to Notify-Gateway API to send SMS to appplicant.
        # TODO - Insert calls to Identity-Gateway API for checking application's SMS code.

        return HttpResponseRedirect(reverse(self.success_url))
