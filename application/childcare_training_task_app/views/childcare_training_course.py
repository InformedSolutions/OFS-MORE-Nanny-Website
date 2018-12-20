from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny.db_gateways import NannyGatewayActions


class ChildcareTrainingCourseView(View):
    """
    Class containing the methods for handling requests to the 'Childcare-Training-Course' page.
    """
    def get(self, request):
        application_id = request.GET['id']
        context = {'id': application_id}
        record = NannyGatewayActions().read('application', params={'application_id':application_id}).record
        record['childcare_training_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=record)
        return render(request, template_name='childcare-training-course.html', context=context)

    def post(self, request):
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + request.GET['id'])
