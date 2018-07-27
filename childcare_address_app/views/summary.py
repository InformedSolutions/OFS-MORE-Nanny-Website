from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from ..utils import build_url
from ..address_helper import *

from nanny_gateway import NannyGatewayActions


class ChildcareAddressSummaryView(View):
    """
    Handle get and post requests to the summary view.
    """
    def get(self, request):
        app_id = request.GET['id']
        context = {
            'id': app_id
        }

        app_record = NannyGatewayActions().read('application', params={'application_id': app_id})

        if app_record['address_to_be_provided']:
            address_to_be_provided = 'Yes'
        else:
            address_to_be_provided = 'No'

        context['address_to_be_provided'] = address_to_be_provided

        address_records = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})

        data = []

        for i in range(1, len(address_records) + 1):
            record = {}
            record['title'] = "Childcare address " + str(i)

            record['address'] = AddressHelper.format_address(address_records[i - 1], "</br>")
            record['change_link'] = build_url('Childcare-Address-Manual-Entry',
                                              get={
                                                  'id': address_records[i - 1]['application_id'],
                                                  'childcare_address_id': address_records[i - 1]['childcare_address_id']
                                              })
            data.append(record)

        context['records'] = data

        # get home address
        record = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})

        home_address = record['childcare_address']
        if home_address:
            context['home_address'] = 'Yes'
        else:
            context['home_address'] = 'No'

        return render(request, template_name='childcare-address-summary.html', context=context)

    def post(self, request):
        app_id = request.GET['id']
        record = NannyGatewayActions().read('application', params={'application_id': app_id})
        record['childcare_address_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=record)
        return HttpResponseRedirect(build_url('Task-List', get={'id': app_id}))
