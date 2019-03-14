import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from application.services.db_gateways import NannyGatewayActions
from application.presentation.table_util import Row, Table
from application.presentation.utilities import build_url


class Summary(View):
    template_name = 'summary.html'
    success_url_name = 'Task-List'

    def get(self, request):
        return render(request, 'generic-summary-template.html', context=self.get_context_data())

    def post(self, request):
        application_id = self.request.POST['id']
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        application_record['first_aid_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=application_record)
        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))

    def get_context_data(self):
        context = dict()
        application_id = self.request.GET['id']
        first_aid_response = NannyGatewayActions().read('first-aid', params={'application_id': application_id})
        if first_aid_response.status_code == 200:
            first_aid_record = first_aid_response.record
            course_date = datetime.datetime.strptime(first_aid_record['course_date'], '%Y-%m-%d').date()
            formatted_course_date = course_date.strftime('%d/%m/%Y')

            organisation_row = Row('training_organisation', 'Training organisation',
                                   first_aid_record['training_organisation'], 'first-aid:Training-Details',
                                   "training organisation")
            course_title_row = Row('course_title', 'Title of training course', first_aid_record['course_title'],
                                   'first-aid:Training-Details', "course title")
            course_date_row = Row('course_date', 'Date you completed the course', formatted_course_date,
                                  'first-aid:Training-Details', "course completion date")

            first_aid_table = Table(application_id)
            first_aid_table.row_list = [organisation_row, course_title_row, course_date_row]
            first_aid_table.get_errors()

            context['table_list'] = [first_aid_table]
            context['application_id'] = application_id
            context['page_title'] = 'Check your answers: first aid training'
            context['link_url'] = build_url(self.success_url_name, get={'id': application_id})
            context['id'] = self.request.GET['id']
            context['first_aid_record'] = first_aid_record
        else:
            raise Exception("A matching first aid record couldn't be found.")
        return context
