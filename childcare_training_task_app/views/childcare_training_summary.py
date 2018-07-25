from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny_gateway import NannyGatewayActions

class ChildcareTrainingSummaryView(View):
    """
    Class containing the methods for handling requests to the 'Childcare-Training-Summary' page.
    """
    def get(self, request):
        application_id = request.GET['id']
        record = NannyGatewayActions().read('childcare-training', params={'application_id': application_id})
        context = {'id': application_id, 'record': record}
        return render(request, template_name='childcare-training-summary.html', context=context)

    def post(self, request):
        application_id = request.GET['id']
        record = NannyGatewayActions().read('application', params={'application_id': application_id})
        record['childcare_training_status'] = "COMPLETED"
        NannyGatewayActions().put('application', params=record)
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + application_id)
