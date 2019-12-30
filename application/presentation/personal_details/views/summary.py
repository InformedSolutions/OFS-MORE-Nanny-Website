import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from application.presentation.table_util import Row, Table
from application.presentation.utilities import build_url, app_id_finder
from application.services.address_helper import AddressHelper
from application.services.db_gateways import NannyGatewayActions


class Summary(View):
    template_name = 'generic-summary-template.html'
    success_url_name = 'Task-List'

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        application_id = app_id_finder(request)
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        application_record['personal_details_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=application_record)

        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))

    def get_context_data(self):
        context = dict()
        application_id = app_id_finder(self.request)
        personal_details_record = NannyGatewayActions().read('applicant-personal-details',
                                                             params={'application_id': application_id}).record
        address_record = NannyGatewayActions().read('applicant-home-address',
                                                    params={'application_id': application_id}).record
        name = personal_details_record['first_name'] + ' ' + personal_details_record['middle_names'] + ' ' + \
               personal_details_record['last_name']

        date_of_birth_datetime = datetime.datetime.strptime(personal_details_record['date_of_birth'], '%Y-%m-%d')
        date_of_birth = date_of_birth_datetime.strftime('%d/%m/%Y')

        address = AddressHelper.format_address(address_record, ", ")
        known_to_social_services = personal_details_record['known_to_social_services']
        reasons_known_to_social_services = personal_details_record['reasons_known_to_social_services']

        title_row = Row('title', 'Title', personal_details_record['title'], 'personal-details:Personal-Details-Name', 'title')
        name_row = Row('name', 'Your name', name, 'personal-details:Personal-Details-Name', "your name")
        date_of_birth_row = Row('date_of_birth', 'Date of birth', date_of_birth,
                                'personal-details:Personal-Details-Date-Of-Birth', "your date of birth")
        home_address_row = Row('home_address', 'Your home address', address,
                               'personal-details:Personal-Details-Manual-Address', "your home address")
        known_to_social_services_row = Row('known_to_social_services', 'Known to council social Services?',
                                           known_to_social_services,
                                           'personal-details:Personal-Details-Your-Children',
                                           "answer to known to council social services in regards to your own children")
        reasons_known_to_social_services_row = Row('reasons_known_to_social_services', 'Tell us why',
                                                   reasons_known_to_social_services,
                                                   'personal-details:Personal-Details-Your-Children',
                                                   "why you are known to council social services in regards to your own children")

        personal_details_table = Table(application_id)

        # Older applications won't have this - only try to do stuff if the date exists
        if personal_details_record['moved_in_date']:
            moved_in_date_datetime = datetime.datetime.strptime(personal_details_record['moved_in_date'],
                                                                '%Y-%m-%d').date()
            moved_in_date = moved_in_date_datetime.strftime('%d/%m/%Y')

            moved_in_date_row = Row('moved_in_date', 'Moved in date', moved_in_date,
                                    'personal-details:Personal-Details-Manual-Address', 'moved in date')
            personal_details_table.row_list = [title_row, name_row, date_of_birth_row, home_address_row, moved_in_date_row,
                                            known_to_social_services_row]
        else:
            personal_details_table.row_list = [title_row, name_row, date_of_birth_row, home_address_row,
                                               known_to_social_services_row]

        if known_to_social_services:
            personal_details_table.row_list.append(reasons_known_to_social_services_row)

        personal_details_table.get_errors(['applicant-personal-details', 'applicant-home-address'])

        context['table_list'] = [personal_details_table]
        context['id'] = application_id
        context['application_id'] = application_id
        context['page_title'] = 'Check your answers: your personal details'
        return context
