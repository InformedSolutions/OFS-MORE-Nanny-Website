from nanny.base_views import BaseTemplateView
from nanny.utilities import *

from nanny_gateway import NannyGatewayActions


class Confirmation(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "confirmation.html"

    def get_context_data(self, **kwargs):
        app_id = app_id_finder(self.request)
        context = {}

        pd_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': app_id})
        context['lived_abroad'] = pd_record['lived_abroad']
        app_record = NannyGatewayActions().read('application', params={'application_id', app_id})
        context['application_reference'] = app_record['application_reference']
        context['id'] = app_id
        return context
