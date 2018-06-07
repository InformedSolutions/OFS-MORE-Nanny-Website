from identity_models.user_details import UserDetails

from login_app.forms import SecurityCodeForm

from .base import BaseFormView


class SecurityCodeFormView(BaseFormView):
    """
    Class containing the methods for handling requests to the 'Security-Code' page.
    """
    template_name = 'security-code.html'
    form_class = SecurityCodeForm
    success_url = 'Contact-Details-Summary'  # TODO: Replace this with Task List once that view is built.

    def get_form_kwargs(self):
        kwargs = super(SecurityCodeFormView, self).get_form_kwargs()
        kwargs['correct_sms_code'] = UserDetails.api.get_record(email=self.request.GET['email_address']).record['magic_link_sms']
        return kwargs
