from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny_models.nanny_application import NannyApplication
from nanny_models.childcare_training import ChildcareTraining


class ChildcareTrainingSummaryView(View):
    """
    Class containing the methods for handling requests to the 'Childcare-Training-Summary' page.
    """
    def get(self, request):
        application_id = request.GET['id']
        nanny_api_response = ChildcareTraining.api.get_record(application_id=application_id)
        context = {'id': application_id, 'record': nanny_api_response.record}
        return render(request, template_name='childcare-training-summary.html', context=context)

    def post(self, request):
        application_id = request.GET['id']
        record = NannyApplication.api.get_record(application_id=application_id).record
        record['childcare_training_status'] = "COMPLETED"
        NannyApplication.api.put(record)
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + application_id)
