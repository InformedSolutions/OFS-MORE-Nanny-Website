from identity_models.user_details import UserDetails

from middleware import CustomAuthenticationHandler
from login_app import login_redirect_helper

from login_app.forms import SecurityCodeForm

from .base import BaseFormView


class SecurityCodeFormView(BaseFormView):
    """
    Class containing the methods for handling requests to the 'Security-Code' page.
    """
    template_name = 'security-code.html'
    form_class = SecurityCodeForm
    success_url = 'Contact-Details-Summary'  # TODO: Replace this with Task List once that view is built.

    def form_valid(self, form):
        application_id = self.request.GET['id']
        record = UserDetails.api.get_record(application_id=application_id).record
        record['sms_resend_attempts'] = 0
        UserDetails.api.put(record)
        record = UserDetails.api.get_record(application_id=application_id).record
        response = login_redirect_helper.redirect_by_status(record['application_id'])
        CustomAuthenticationHandler.create_session(response, record['email'])
        return response

    def get_form_kwargs(self):
        kwargs = super(SecurityCodeFormView, self).get_form_kwargs()
        kwargs['correct_sms_code'] = UserDetails.api.get_record(application_id=self.request.GET['id']).record['magic_link_sms']
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super(SecurityCodeFormView, self).get_context_data()
        application_id = self.request.GET['id']
        record = UserDetails.api.get_record(application_id=application_id).record
        kwargs['mobile_number_end'] = record['mobile_number'][-3:]
        kwargs['application_id'] = application_id  # Pass to context for the hyperlinks.
        kwargs['sms_resend_attempts'] = record['sms_resend_attempts']

        # Template requires knowledge of whether or not the SMS was resent.
        # If they have come from email valdiation link, the request.META.get('HTTP_REFERER') is None.
        if self.request.META.get('HTTP_REFERER') is not None:
            kwargs['code_resent'] = True
        else:
            kwargs['code_resent'] = False

        return kwargs
