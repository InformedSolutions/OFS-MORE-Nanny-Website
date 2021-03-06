from django.http import HttpResponseRedirect

from application.presentation.base_views import NannyTemplateView
from application.services.db_gateways import NannyGatewayActions
from application.presentation.utilities import app_id_finder, build_url


class CriminalRecordsCheckGuidanceView(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = 'criminal-record-checks-guidance.html'
    success_url_name = 'dbs:Lived-Abroad-View'

    def post(self, request):
        application_id = app_id_finder(request)
        NannyGatewayActions().patch('application', params={'application_id': application_id, 'dbs_status': 'IN_PROGRESS'})
        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))
