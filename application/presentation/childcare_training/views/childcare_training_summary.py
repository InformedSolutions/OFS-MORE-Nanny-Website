from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny.db_gateways import NannyGatewayActions
from nanny.table_util import Row, Table


class ChildcareTrainingSummaryView(View):
    """
    Class containing the methods for handling requests to the 'Childcare-Training-Summary' page.
    """
    def get(self, request):
        return render(request, template_name='generic-summary-template.html', context=self.get_context_data())

    def post(self, request):
        application_id = request.GET['id']
        record = NannyGatewayActions().read('application', params={'application_id':application_id}).record
        record['childcare_training_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=record)
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + application_id)

    def get_context_data(self):
        context = dict()
        application_id = self.request.GET['id']
        childcare_record = NannyGatewayActions().read('childcare-training', params={'application_id': application_id}).record

        level_2_training     = childcare_record['level_2_training']
        common_core_training = childcare_record['common_core_training']

        if level_2_training and common_core_training:
            row_value = 'Childcare qualification (level 2 or higher) and training in common core skills'
        elif level_2_training:
            row_value = 'Childcare qualification (level 2 or higher)'
        else:
            row_value = 'Training in common core skills'

        childcare_training_row = Row('childcare_training', 'What type of childcare course have you completed?', row_value, 'Type-Of-Childcare-Training', None)

        childcare_training_summary_table = Table(application_id)
        childcare_training_summary_table.row_list = [childcare_training_row]
        childcare_training_summary_table.get_errors()

        context['table_list'] = [childcare_training_summary_table]
        context['application_id'] = application_id
        context['id'] = application_id
        context['page_title'] = 'Check your answers: childcare training'

        context['record'] = childcare_record

        return context
