from ..forms import PhoneNumbersForm

from nanny.middleware import CustomAuthenticationHandler
from django.http import HttpResponseRedirect
from .base import BaseFormView
from application.presentation.utilities import app_id_finder, build_url
from application.services.db_gateways import IdentityGatewayActions


class PhoneNumbersFormView(BaseFormView):
    """
    Class for handling requests to the 'Phone-Number' page.
    """
    template_name = 'phone-number.html'
    form_class = PhoneNumbersForm
    success_url = 'Contact-Details-Summary'

    def form_valid(self, form):
        application_id = self.request.GET['id']
        api_response = IdentityGatewayActions().read('user', params={'application_id': application_id})

        record = api_response.record
        record['mobile_number'] = form.cleaned_data['mobile_number']
        record['add_phone_number'] = form.cleaned_data['other_phone_number']

        IdentityGatewayActions().put('user', params=record)

        response = HttpResponseRedirect(build_url('Contact-Details-Summary', get={'id': application_id}))

        COOKIE_IDENTIFIER = CustomAuthenticationHandler.get_cookie_identifier()

        if COOKIE_IDENTIFIER not in self.request.COOKIES:
            CustomAuthenticationHandler.create_session(response, record['email'])
            return response

        return super(PhoneNumbersFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]

        context = super(PhoneNumbersFormView, self).get_context_data(**kwargs)
        context['id'] = app_id_finder(self.request)
        return context

    def get_initial(self):
        application_id = self.request.GET['id']
        record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
        initial_values = {
            'mobile_number': record['mobile_number'],
            'other_phone_number': record['add_phone_number']
        }
        return initial_values
