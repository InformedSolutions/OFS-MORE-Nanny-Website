from application.presentation.base_views import NannyTemplateView
from application.presentation.utilities import *

from ....services.notify import send_email
from ....services.db_gateways import NannyGatewayActions, IdentityGatewayActions
import logging

logger = logging.getLogger()


class Confirmation(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "confirmation.html"

    def get_context_data(self, **kwargs):
        app_id = app_id_finder(self.request)
        context = {}
        api_pd_response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': app_id})

        if api_pd_response.status_code == 200:
            record = api_pd_response.record
            context['lived_abroad'] = record['lived_abroad']

        api_app_response = NannyGatewayActions().read('application', params={'application_id': app_id})

        if api_app_response.status_code == 200:
            record = api_app_response.record
            context['application_reference'] = record['application_reference']

            # Check for ARC_REVIEW to prevent resetting the status of apps assigned to a reviewer.
            if record['application_status'] != 'ARC_REVIEW':
                record['application_status'] = 'SUBMITTED'
                NannyGatewayActions().put('application', params=record)

        if api_pd_response.status_code == 200 and api_app_response.status_code == 200:
            personal_details_record = api_pd_response.record
            application_record = api_app_response.record
            self.send_survey_email(app_id, personal_details_record, application_record)

        context['id'] = app_id
        return context

    @staticmethod
    def send_survey_email(application_id, personal_details_record, application_record):
        """
        function to get user's details and send them the survey email on confirmation of their payment
        :param application_id:
        :param personal_details_record:
        :param application_record:
        """
        survey_template_id = 'ca1acc2f-cfc7-4d20-b5d6-5bb17fce1d0a'
        user_details_response = IdentityGatewayActions().read('user', params={'application_id': application_id})

        if user_details_response.status_code == 200:
            email = user_details_response.record['email']

            survey_personalisation = {
                'first_name': personal_details_record['first_name'], 'ref': application_record['application_reference']
            }

            logger.debug("Attempting to send survey email: What do you think of our service? - Applicant")
            send_email(email, survey_personalisation, survey_template_id)


