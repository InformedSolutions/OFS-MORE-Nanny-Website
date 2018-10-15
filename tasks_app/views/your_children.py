from django.http import HttpResponseRedirect
from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView


class YourChildrenGuidance(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "your_children_guidance.html"
    success_url_name = 'Task-List'

    def post(self, request):

        app_id = app_id_finder(self.request)
        # update task status to be done
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'COMPLETED'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('Task-List', get={'id': app_id}))
