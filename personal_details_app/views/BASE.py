from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render

from ..utils import build_url


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
        # If user was on first sign-in page, email_address won't be stored in GET request QueryDict. In that case, the
        # email_address will be stored in POST request QueryDict.

        success_params = {}
        if 'email_address' in self.request.GET.keys():
            success_params['email_address'] = self.request.GET['email_address']
        elif 'email_address' in self.request.GET.keys():
            success_params['email_address'] = self.request.POST['email_address']

        if 'id' in self.request.GET.keys():
            success_params['id'] = self.request.GET['id']
        elif 'id' in self.request.GET.keys():
            success_params['id'] = self.request.POST['id']

        return success_params


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)
        app_id = self.request.GET.get('id')
        context['application_id'] = app_id
        return context


class ServiceUnavailableView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Service-Unavailable' page.
    """

    def get(self, request):
        return render(request, 'service-unavailable.html')