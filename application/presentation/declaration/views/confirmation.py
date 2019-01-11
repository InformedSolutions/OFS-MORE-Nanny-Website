from application.presentation.base_views import NannyTemplateView
from application.presentation.utilities import *

from application.services.db_gateways import NannyGatewayActions


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

        context['id'] = app_id
        return context
