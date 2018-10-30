from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from nanny.db_gateways import NannyGatewayActions
from nanny.table_util import Row, Table

from ..address_helper import *
from ..utils import build_url


class ChildcareAddressSummaryView(View):
    """
    Handle get and post requests to the summary view.
    """
    def get(self, request):

        # context = {
        #     'id': app_id
        # }
        #
        # app_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        # if app_response.status_code == 200:
        #
        #     app_record = app_response.record
        #     if app_record['address_to_be_provided']:
        #         address_to_be_provided = 'Yes'
        #     else:
        #         address_to_be_provided = 'No'
        #
        #     context['address_to_be_provided'] = address_to_be_provided
        #
        #     address_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
        #
        #     if address_response.status_code == 200:
        #         address_records = address_response.record
        #
        #         data = []
        #
        #         for i in range(1, len(address_records) + 1):
        #             record = {}
        #             record['title'] = "Childcare address " + str(i)
        #
        #             record['address'] = AddressHelper.format_address(address_records[i - 1], "</br>")
        #             record['change_link'] = build_url('Childcare-Address-Details',
        #                                               get={
        #                                                   'id': address_records[i - 1]['application_id'],
        #                                               })
        #             data.append(record)
        #
        #         context['records'] = data
        #
        # # get home address
        # home_address_resp = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
        # if home_address_resp.status_code == 200:
        #     home_address = home_address_resp.record['childcare_address']
        #     if home_address is not None:
        #         if home_address:
        #             context['home_address'] = 'Yes'
        #         else:
        #             context['home_address'] = 'No'
        #     else:
        #         context['home_address'] = None

        return render(request, template_name='generic-summary-template.html', context=self.get_context_data())

    def post(self, request):
        app_id = request.GET['id']
        api_response = NannyGatewayActions().read(
            'application',
            params={'application_id': app_id}
        )
        api_response.record['childcare_address_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=api_response.record)
        return HttpResponseRedirect(build_url('Task-List', get={'id': app_id}))

    def get_context_data(self):
        context = dict()

        application_id = self.request.GET['id']

        app_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record

        if app_record['address_to_be_provided']:
            address_to_be_provided = 'Yes'
        else:
            address_to_be_provided = 'No'

        known_childcare_location_row = Row('address_to_be_provided', 'Do you know where you\'ll be working?', address_to_be_provided, 'Childcare-Address-Where-You-Work', None)

        childcare_address_summary_table = Table(application_id)
        childcare_address_summary_table.row_list = [known_childcare_location_row]
        childcare_address_summary_table.get_errors()

        context['table_list'] = [childcare_address_summary_table]
        context['application_id'] = application_id
        context['id'] = application_id
        context['page_title'] = 'Check your answers: childcare location'

        return context
