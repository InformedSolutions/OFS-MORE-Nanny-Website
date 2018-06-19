from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny_models.application import Application


class ChildcareTrainingSummaryView(View):
    def get(self, request):
        return render(request, template_name='childcare-training-summary.html')

    def post(self, request):
        application_id = request.GET['id']
        record = Application.api.get_record(application_id=application_id).record
        record['childcare_training_status'] = "COMPLETED"
        Application.api.put(record)
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + application_id)
