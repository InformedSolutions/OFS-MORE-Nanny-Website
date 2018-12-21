from nanny.middleware import CustomAuthenticationHandler
from . import login_redirect_helper

from ..forms import DBSSecurityQuestionForm, PersonalDetailsSecurityQuestionForm, MobileNumberSecurityQuestionForm

from .base import BaseFormView

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


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
        app_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        personal_details_record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record

        if app_record is None:
            form = MobileNumberSecurityQuestionForm
        elif app_record['dbs_status'] == 'COMPLETED':
            form = DBSSecurityQuestionForm
        elif app_record['personal_details_status'] == 'COMPLETED':
            form = PersonalDetailsSecurityQuestionForm
        elif len(personal_details_record['mobile_number']) != 0:
            form = MobileNumberSecurityQuestionForm

        self.form_class = form

        return form

    def get_security_question_answer(self):
        application_id = self.request.GET['id']

        if self.form_class == MobileNumberSecurityQuestionForm:
            return {
                'mobile_number': IdentityGatewayActions().read('user', params={'application_id': application_id}).record['mobile_number']
            }

        elif self.form_class == PersonalDetailsSecurityQuestionForm:
            personal_details_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id}).record
            childcare_address_record = NannyGatewayActions().read('applicant-home-address', params={'application_id': application_id}).record
            return {
                'date_of_birth': personal_details_record['date_of_birth'],
                'postcode': childcare_address_record['postcode'],
            }

        elif self.form_class == DBSSecurityQuestionForm:
            return {
                'dbs_number': NannyGatewayActions().read('dbs-check', params={'application_id': application_id}).record['dbs_number']
            }

    def get_form(self, form_class=None):
        self.get_security_question_form()
        form = super(SecurityQuestionFormView, self).get_form()
        form.correct_answer = self.get_security_question_answer()
        return form

    def form_valid(self, form):
        application_id = self.request.GET['id']
        record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
        record['sms_resend_attempts'] = 0
        IdentityGatewayActions().put('user', params=record)
        response = login_redirect_helper.redirect_by_status(record['application_id'])
        CustomAuthenticationHandler.create_session(response, record['email'])
        return response
