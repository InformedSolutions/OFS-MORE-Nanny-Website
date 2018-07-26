import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from ..address_helper import AddressHelper

from ..utils import build_url

from nanny_gateway import NannyGatewayActions


class Summary(View):

    template_name = 'personal_details_summary.html'
    success_url_name = 'Task-List'

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        application_id = self.request.POST['id']
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id})
        application_record['personal_details_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', application_record)

        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))

    def get_context_data(self, **kwargs):
        context = {}
        application_id = self.request.GET['id']
        context['link_url'] = build_url(self.success_url_name, get={'id': application_id})
        context['application_id'] = application_id
        context['id'] = application_id
        temp_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
        temp_record['date_of_birth'] = datetime.datetime.strptime(temp_record['date_of_birth'], '%Y-%m-%d')
        context['personal_details_record'] = temp_record

        # ADD PERSONAL ADDRESS RECORD HERE
        address = NannyGatewayActions().read('applicant-home-address', params={'application_id': application_id})
        context['personal_address_record'] = AddressHelper.format_address(address, ", ")
        return context

