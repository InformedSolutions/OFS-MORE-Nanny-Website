from django.views.generic import FormView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from login_app.forms import AcccountSelectionForm


class AccountSelectionFormView(FormView):
    """
    Class containing the methods for handling requests to the 'Account-Selection' page.
    """
    template_name = 'account-selection.html'
    form_class = AcccountSelectionForm

    def form_valid(self, request):

        if request.cleaned_data['account_selection'] == 'new':
            self.success_url = reverse('New-User-Sign-In')
        elif request.cleaned_data['account_selection'] == 'existing':
            self.success_url = reverse('Existing-User-Sign-In')

        return HttpResponseRedirect(self.get_success_url())
