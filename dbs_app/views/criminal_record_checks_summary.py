from django.http import HttpResponseRedirect

from nanny.base_views import NannyTemplateView
from nanny.db_gateways import NannyGatewayActions
from nanny.table_util import Row, Table
from nanny.utilities import app_id_finder, build_url


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
        application_id = request.POST['id']
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        application_record['dbs_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=application_record)

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

        dbs_row = Row('dbs_number', 'DBS certificate number', dbs_record['dbs_number'], 'dbs:Details', None)
        convictions_row = Row('convictions', 'Do you have any criminal cautions or convictions?', dbs_record['convictions'], 'dbs:Details', None)

        dbs_summary_table = Table(application_id)
        dbs_summary_table.row_list = [dbs_row, convictions_row]
        dbs_summary_table.get_errors()
        table_list = [dbs_summary_table]

        context['id'] = self.request.GET['id']

        context['table_list'] = table_list
        context['application_id'] = application_id
        context['page_title'] = 'Check your answers: criminal record (DBS) check'

        return context
