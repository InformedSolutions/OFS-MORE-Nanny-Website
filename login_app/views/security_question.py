from identity_models.user_details import UserDetails

from middleware import CustomAuthenticationHandler
from login_app import login_redirect_helper

from login_app.forms import DBSSecurityQuestionForm, DoBSecurityQuestionForm, MobileNumberSecurityQuestionForm

from .base import BaseFormView


class SecurityQuestionFormView(BaseFormView):
    """
    Class for handling requests to the 'Security-Question' page.
    """
    template_name = 'security-question.html'
    form_class = None
    success_url = 'Contact-Details-Summary'

    def get_security_question_form(self, application):
        """
        Pseudo-code for getting the security question for a given applicant, depending upon the status of their
        application.
        """

        # TODO: Add API calls to execute the below once Application API built.

        acc = application.user_details
        if application.criminal_record_check_status == 'COMPLETED':
            form = DBSSecurityQuestionForm
        elif application.personal_details_status == 'COMPLETED':
            form = DoBSecurityQuestionForm
        elif len(acc.mobile_number) != 0:
            form = MobileNumberSecurityQuestionForm
        return form

    def get_security_question_answer(self):
        return UserDetails.api.get_record(email=self.request.GET['email_address']).record['mobile_number']

    def get_form(self, form_class=None):
        form = super(SecurityQuestionFormView, self).get_form()
        form.correct_answer = self.get_security_question_answer()
        return form

    def form_valid(self, form):
        record = UserDetails.api.get_record(email=self.request.GET['email_address']).record
        record['sms_resend_attempts'] = 0
        UserDetails.api.put(record)
        record = UserDetails.api.get_record(email=self.request.GET['email_address']).record
        response = login_redirect_helper.redirect_by_status(record['application_id'])
        CustomAuthenticationHandler.create_session(response, record['email'])
        return response

    def __init__(self, *args, **kwargs):
        # self.form_class = self.get_security_question_form()
        # TODO: Uncomment above once the Application API functional
        self.form_class = MobileNumberSecurityQuestionForm
        super(SecurityQuestionFormView, self).__init__(*args, **kwargs)
