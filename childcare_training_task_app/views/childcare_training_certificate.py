from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny.db_gateways import NannyGatewayActions


class ChildcareTrainingCertificateView(View):
    """
    Class containing the methods for handling requests to the 'Childcare-Training-Certificate' page.
    """
    def get(self, request):
        context = {'id': request.GET['id']}
        application_id = request.GET['id']
        record = NannyGatewayActions().read('application', params={'application_id':application_id}).record
        record['childcare_training_status'] = 'IN_PROGRESS'
        return render(request, template_name='childcare-training-certificate.html', context=context)

    def post(self, request):
        application_id = request.GET['id']
        record = NannyGatewayActions().read('application', params={'application_id':application_id}).record
        record['childcare_training_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=record)
        return HttpResponseRedirect(reverse('Childcare-Training-Summary') + '?id=' + application_id)
