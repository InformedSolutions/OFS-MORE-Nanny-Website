from application.presentation.base_views import NannyTemplateView
from application.presentation.utilities import *

from application.services.db_gateways import NannyGatewayActions


class Confirmation(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """

    def get_context_data(self, **kwargs):
        app_id = app_id_finder(self.request)
        cost = '103.00'
        api_app_response = NannyGatewayActions().read('application', params={'application_id': app_id})

        context = {
            'id': app_id,
            'cost': cost
        }

        if api_app_response.status_code == 200:
            record = api_app_response.record
            context['application_reference'] = record['application_reference']

            # Check for ARC_REVIEW to prevent resetting the status of apps assigned to a reviewer.
            if record['application_status'] != 'ARC_REVIEW':
                record['application_status'] = 'SUBMITTED'
                NannyGatewayActions().put('application', params=record)
        else:
            raise ValueError('Nanny-Gateway returned {0} response for "application" endpoint, not 200'.format(
                api_app_response.status_code))

        return context

    def get_template_names(self):
        app_id = app_id_finder(self.request)
        dbs_record = NannyGatewayActions().read('dbs-check', params={'application_id': app_id}).record
        personal_details_record = NannyGatewayActions().read('applicant-personal-details',
                                                             params={'application_id': app_id}).record

        capita = dbs_record['is_ofsted_dbs']
        certificate_information = dbs_record['certificate_information']
        lived_abroad = personal_details_record['lived_abroad']

        confirmation_status = get_confirmation_status(capita, certificate_information, lived_abroad)
        template_name = get_confirmation_page_template(confirmation_status)

        return [template_name]
