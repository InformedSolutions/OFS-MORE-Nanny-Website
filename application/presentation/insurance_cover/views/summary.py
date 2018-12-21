from application.presentation.base_views import NannyTemplateView
from django.http import HttpResponseRedirect
from application.presentation.utilities import *

from application.services.db_gateways import NannyGatewayActions
from application.presentation.table_util import Row, Table


class SummaryView(NannyTemplateView):
    template_name = 'generic-summary-template.html'
    success_url_name = 'Task-List'

    def post(self, request):
        app_id = app_id_finder(self.request)
        # update task status to be done
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['insurance_cover_status'] = 'COMPLETED'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('Task-List', get={'id': app_id}))

    def get_context_data(self):
        context = dict()
        application_id = app_id_finder(self.request)
        insurance_record = NannyGatewayActions().read('insurance-cover',
                                                      params={'application_id': application_id}).record

        insurance_row = Row('public_liability', 'Do you have public liability insurance?',
                            insurance_record['public_liability'], 'insurance:Public-Liability',
                            "answer on having public liability insurance")

        insurance_summary_table = Table(application_id)
        insurance_summary_table.row_list = [insurance_row, ]
        insurance_summary_table.get_errors()

        context['table_list'] = [insurance_summary_table]
        context['application_id'] = application_id
        context['page_title'] = 'Check your answers: insurance cover'

        context['id'] = self.request.GET['id']
        return context
