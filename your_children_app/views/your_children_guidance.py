from django.http import HttpResponseRedirect
from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView


class YourChildrenGuidanceView(NannyTemplateView):
    """
    Template view to  render the your children details view
    """
    template_name = "your-children-guidance.html"
    success_url_name = 'your-children:Your-Children-Details'

    def post(self, request):

        app_id = app_id_finder(self.request)
        # update task status to be done
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('your-children:Your-Children-Details', get={'id': app_id}))
