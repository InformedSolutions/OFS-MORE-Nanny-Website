import datetime
from nanny.middleware import CustomAuthenticationHandler
from application.presentation.login import login_redirect_helper

from ..forms import SecurityCodeForm

from .base import BaseFormView

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


class SecurityCodeFormView(BaseFormView):
    """
    Class containing the methods for handling requests to the 'Security-Code' page.
    """
    template_name = 'security-code.html'
    form_class = SecurityCodeForm
    success_url = 'Contact-Details-Summary'  # TODO: Replace this with Task List once that view is built.

    def form_valid(self, form):
        application_id = self.request.GET['id']
        record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
        record['sms_resend_attempts'] = 0
        record['email_expiry_date'] = 0
        IdentityGatewayActions().put('user', params=record)
        response = login_redirect_helper.redirect_by_status(record['application_id'])
        CustomAuthenticationHandler.create_session(response, record['email'])

        # Update last accessed time when successfully signed in
        nanny_actions = NannyGatewayActions()
        app_response = nanny_actions.read('application', params={'application_id': application_id})
        if app_response.status_code == 200 and hasattr(app_response, 'record'):
            # application might not exist yet, if user signed out before completing contact details task
            application = app_response.record
            application['date_last_accessed'] = datetime.datetime.now()
            application['application_expiry_email_sent'] = False
            nanny_actions.put('application', application)


        return response

    def get_form_kwargs(self):
        kwargs = super(SecurityCodeFormView, self).get_form_kwargs()
        kwargs['correct_sms_code'] = IdentityGatewayActions().read(
            'user', params={'application_id': self.request.GET['id']}).record['magic_link_sms']
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super(SecurityCodeFormView, self).get_context_data()
        application_id = self.request.GET['id']
        record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
        kwargs['mobile_number_end'] = record['mobile_number'][-3:]
        kwargs['application_id'] = application_id  # Pass to context for the hyperlinks.
        kwargs['sms_resend_attempts'] = record['sms_resend_attempts']

        # Template requires knowledge of whether or not the SMS was resent.
        # If they have come from email validation link, the request.META.get('HTTP_REFERER') is None.
        if self.request.META.get('HTTP_REFERER') is not None:
            kwargs['code_resent'] = True
        else:
            kwargs['code_resent'] = False

        return kwargs
