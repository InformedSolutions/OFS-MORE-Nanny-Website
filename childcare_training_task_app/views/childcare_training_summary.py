from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny_models.application import Application
from nanny_models.childcare_training import ChildcareTraining


class ChildcareTrainingSummaryView(View):
    def get(self, request):
        application_id = request.GET['id']
        nanny_api_response = ChildcareTraining.api.get_record(application_id=application_id)
        context = {'id': application_id, 'record': nanny_api_response.record}
        return render(request, template_name='childcare-training-summary.html', context=context)

    def post(self, request):
        application_id = request.GET['id']
        record = Application.api.get_record(application_id=application_id).record
        record['childcare_training_status'] = "COMPLETED"
        Application.api.put(record)
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + application_id)
