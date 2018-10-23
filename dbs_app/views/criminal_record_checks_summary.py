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
        application_id = app_id_finder(request)
        NannyGatewayActions().patch('dbs-check', params={'application_id': application_id, 'dbs_status': 'COMPLETED'})
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

        if dbs_record['is_ofsted_dbs'] == 'True':
            dbs_page_link = 'dbs:Capita-DBS-Details-View'
        elif dbs_record['is_ofsted_dbs'] == 'False':
            dbs_page_link = 'dbs:Non-Capita-DBS-Details-View'
        else:
            raise ValueError('The "is_ofsted_dbs" value does not equal either "True" or "False".')

        lived_abroad_row = Row('lived_abroad', 'Have you lived outside of the UK in the last 5 years?', dbs_record['lived_abroad'], 'dbs:Lived-Abroad-View', None)
        ofsted_dbs = Row('is_ofsted_dbs', 'Do you have an Ofsted DBS Check?', dbs_record['is_ofsted_dbs'], 'dbs:DBS-Type-View', "Change answer to having an Ofsted DBS Check")
        dbs_update_service_row = Row('on_dbs_update_service', 'Are you on the DBS update service?', dbs_record['on_dbs_update_service'], 'dbs:DBS-Update-Service-Page', "Change answer to being on the DBS update service")
        dbs_number_row = Row('dbs_number', 'DBS certificate number', dbs_record['dbs_number'], dbs_page_link, None)
        has_convictions_row = Row('has_convictions', 'Do you have any criminal cautions or convictions?', dbs_record['has_convictions'], 'dbs:Capita-DBS-Details-View', None)

        if dbs_record['is_ofsted_dbs'] == 'True':
            row_list = [lived_abroad_row, ofsted_dbs, dbs_number_row, has_convictions_row]
        elif dbs_record['is_ofsted_dbs'] == 'False':
            row_list = [lived_abroad_row, ofsted_dbs, dbs_update_service_row, dbs_number_row]

        dbs_summary_table = Table(application_id)
        dbs_summary_table.row_list = row_list
        dbs_summary_table.get_errors()
        table_list = [dbs_summary_table]

        context['id'] = self.request.GET['id']
        context['table_list'] = table_list
        context['application_id'] = application_id
        context['page_title'] = 'Check your answers: criminal record checks'

        return context
