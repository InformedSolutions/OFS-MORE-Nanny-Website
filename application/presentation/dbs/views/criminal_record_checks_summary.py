from django.http import HttpResponseRedirect

from application.presentation.base_views import NannyTemplateView
from application.services.db_gateways import NannyGatewayActions
from application.presentation.table_util import Row, Table
from application.presentation.utilities import app_id_finder, build_url


class CriminalRecordChecksSummaryView(NannyTemplateView):
    """
    View to render the DBS summary page and act on post requests accordingly
    """
    template_name = 'generic-summary-template.html'
    success_url_name = 'Task-List'

    def post(self, request):
        """
        On a post request, set the task status to completed and redirect the user to the task list
        :return:
        """
        application_id = app_id_finder(request)
        NannyGatewayActions().patch('application', params={'application_id': application_id, 'dbs_status': 'COMPLETED'})
        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))

    def get_context_data(self, **kwargs):
        """
        Grab the redirect url to the task list, the application id, and the full dbs record (render order occurs in
        the template)
        :param kwargs:
        :return:
        """
        context = dict()
        application_id = app_id_finder(self.request)
        dbs_record = NannyGatewayActions().read('dbs-check', params={'application_id': application_id}).record

        dbs_page_link = 'dbs:Capita-DBS-Details-View'

        lived_abroad_row = Row(
            'lived abroad', 'Have you lived outside of the UK in the last 5 years?',
            dbs_record['lived_abroad'], 'dbs:Lived-Abroad-View', 'answer on lived abroad'
        )
        dbs_number_row = Row(
            'dbs_number', 'DBS certificate number',
            dbs_record['dbs_number'], dbs_page_link, 'DBS certificate number'
        )
        dbs_enhanced_check_row = Row(
            'enhanced_check', 'Is it an enhanced DBS check for home-based childcare?',
            dbs_record['enhanced_check'], 'dbs:DBS-Type-View', 'Change answer to DBS being enhanced and home-based'
        )
        dbs_update_service_row = Row(
            'on_dbs_update_service', 'Are you on the DBS update service?',
            dbs_record['on_dbs_update_service'], 'dbs:DBS-Type-View', "Change answer to DBS being on update service"
        )
        if dbs_record['is_ofsted_dbs']:
            if dbs_record['within_three_months']:
                row_list = [lived_abroad_row, dbs_number_row]
            else:
                row_list = [lived_abroad_row, dbs_number_row, dbs_update_service_row]
        elif not dbs_record['is_ofsted_dbs']:
            row_list = [lived_abroad_row, dbs_number_row, dbs_enhanced_check_row, dbs_update_service_row,]

        dbs_summary_table = Table(application_id)
        dbs_summary_table.row_list = row_list
        dbs_summary_table.get_errors()
        table_list = [dbs_summary_table]

        context['id'] = self.request.GET['id']
        context['table_list'] = table_list
        context['application_id'] = application_id
        context['page_title'] = 'Check your answers: criminal record checks'

        return context
