from nanny.base_views import NannyTemplateView
from nanny.utilities import *

from nanny.db_gateways import NannyGatewayActions


class AcceptedConfirmation(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "application-accepted.html"

    def get_context_data(self, **kwargs):
        app_id = app_id_finder(self.request)
        context = {}

        api_app_response = NannyGatewayActions().read('application', params={'application_id': app_id})

        if api_app_response.status_code == 200:
            record = api_app_response.record
            context['application_reference'] = record['application_reference']

        context['id'] = app_id
        return context
