from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View


from nanny_models.application import Application


class ChildcareTrainingGuidanceView(View):
    def get(self, request):
        return render(request, template_name='childcare-training-guidance.html')

    def post(self, request):
        application_id = request.GET['id']
        record = Application.api.get_record(application_id=application_id).record
        record['childcare_training_status'] = "STARTED"
        Application.api.put(application_id=application_id, record=record)
        return HttpResponseRedirect(reverse('Type-Of-Childcare-Training') + '?id=' + application_id)
