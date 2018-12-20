from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.views.generic import FormView

from nanny.utilities import build_url


class BaseFormView(FormView):
    """
    Base class for FormViews which implement or override the methods defined below.
    """
    template_name = None
    form_class = None
    success_url = None

    def get_success_url(self):
        """
        Method to construct a url encoded with the necessary varaibles and navigate to it upone successful submission of
        a form.
        :return: a full url for the next page.
        """

        if self.success_url:
            # If not none, run the build url util function
            return build_url(self.success_url, get=self.get_success_parameters())
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")

    def get_success_parameters(self):
        """
        Method to return a dictionary of parameters to be included as variables in the success url, e.g. application_id.
        """
        return {'id': self.request.GET['id']}
