from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from nanny_gateway import NannyGatewayActions

from first_aid_app.views.base import build_url


class Summary(View):

    template_name = 'summary.html'
    success_url_name = 'Task-List'

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'summary.html', context)

    def post(self, request):
        application_id = self.request.POST['id']
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id})
        application_record['first_aid_training_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', application_record)

        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))

    def get_context_data(self, **kwargs):
        context = {}
        application_id = self.request.GET['id']
        context['link_url'] = build_url(self.success_url_name, get={'id': application_id})
        context['application_id'] = application_id
        context['first_aid_record'] = NannyGatewayActions().read('first_aid_training', params={'application_id': application_id})
        return context