import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from ..address_helper import AddressHelper

from nanny.db_gateways import NannyGatewayActions
from nanny.table_util import Row, Table
from nanny.utilities import build_url


class Summary(View):
    template_name = 'generic-summary-template.html'
    success_url_name = 'Task-List'

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        application_id = self.request.POST['id']
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        application_record['personal_details_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=application_record)

        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))

    def get_context_data(self):
        context = dict()
        application_id = self.request.GET['id']

        personal_details_record = NannyGatewayActions().read('applicant-personal-details',
                                                             params={'application_id': application_id}).record
        address_record = NannyGatewayActions().read('applicant-home-address',
                                                    params={'application_id': application_id}).record

        name = personal_details_record['first_name'] + ' ' + personal_details_record['middle_names'] + ' ' + \
               personal_details_record['last_name']
        date_of_birth = datetime.datetime.strptime(personal_details_record['date_of_birth'], '%Y-%m-%d').date()
        address = AddressHelper.format_address(address_record, ", ")

        name_row = Row('name', 'Your name', name, 'personal-details:Personal-Details-Name', "your name")
        date_of_birth_row = Row('date_of_birth', 'Date of birth', date_of_birth,
                                'personal-details:Personal-Details-Date-Of-Birth', "your date of birth")
        home_address_row = Row('home_address', 'Your home address', address,
                               'personal-details:Personal-Details-Manual-Address', "your home address")
        lived_abroad_row = Row('lived_abroad', 'Have you lived abroad in the last 5 years?',
                               personal_details_record['lived_abroad'],
                               'personal-details:Personal-Details-Lived-Abroad',
                               "answer on living abroad in the last 5 years")

        personal_details_table = Table(application_id)
        personal_details_table.row_list = [name_row, date_of_birth_row, home_address_row, lived_abroad_row]
        personal_details_table.get_errors()

        context['table_list'] = [personal_details_table]
        context['application_id'] = application_id
        context['page_title'] = 'Check your answers: your personal details'
        return context
