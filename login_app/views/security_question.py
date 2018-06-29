from identity_models.user_details import UserDetails
from nanny_models.nanny_application import NannyApplication
# from nanny_models.applicant_personal_details import ApplicantPersonalDetails
# from nanny_models.aaplicant_criminal_record import ApplicantCriminalRecord

from middleware import CustomAuthenticationHandler
from login_app import login_redirect_helper

from login_app.forms import DBSSecurityQuestionForm, PersonalDetailsSecurityQuestionForm, MobileNumberSecurityQuestionForm

from .base import BaseFormView


class SecurityQuestionFormView(BaseFormView):
    """
    Class for handling requests to the 'Security-Question' page.
    """
    template_name = 'security-question.html'
    form_class = None
    success_url = 'Contact-Details-Summary'

    def get_security_question_form(self):
        """
        Grab the security question for a given applicant, depending upon the status of their application.
        """
        application_id = self.request.GET['id']
        app_record = NannyApplication.api.get_record(application_id=application_id).record
        personal_details_record = UserDetails.api.get_record(application_id=application_id).record

        if app_record is None:
            form = MobileNumberSecurityQuestionForm
        elif app_record['criminal_record_check_status'] == 'COMPLETED':
            form = DBSSecurityQuestionForm
        elif app_record['personal_details_status'] == 'COMPLETED':
            form = PersonalDetailsSecurityQuestionForm
        elif len(personal_details_record['mobile_number']) != 0:
            form = MobileNumberSecurityQuestionForm

        self.form_class = form

        return form

    def get_security_question_answer(self):
        # TODO: Fix below to grab correct answer based on type of form.
        return UserDetails.api.get_record(application_id=self.request.GET['id']).record['mobile_number']

    def get_form(self, form_class=None):
        # form = self.get_security_question_form()
        form = super(SecurityQuestionFormView, self).get_form()
        form.correct_answer = self.get_security_question_answer()
        return form

    def form_valid(self, form):
        application_id = self.request.GET['id']
        record = UserDetails.api.get_record(application_id=application_id).record
        record['sms_resend_attempts'] = 0
        UserDetails.api.put(record)
        response = login_redirect_helper.redirect_by_status(record['application_id'])
        CustomAuthenticationHandler.create_session(response, record['email'])
        return response

    def __init__(self, *args, **kwargs):
        # self.form_class = self.get_security_question_form()
        # TODO: Uncomment above once the Application API functional
        self.form_class = MobileNumberSecurityQuestionForm
        super(SecurityQuestionFormView, self).__init__(*args, **kwargs)
