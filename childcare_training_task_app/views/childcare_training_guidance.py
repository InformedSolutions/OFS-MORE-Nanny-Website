from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View


from nanny_models.application import Application


class ChildcareTrainingGuidanceView(View):
    def get(self, request):
        context = {'id': request.GET['id']}
        return render(request, template_name='childcare-training-guidance.html', context=context)

    def post(self, request):
        application_id = request.GET['id']
        record = Application.api.get_record(application_id=application_id).record
        record['childcare_training_status'] = "IN_PROGRESS"
        Application.api.put(record=record)
        return HttpResponseRedirect(reverse('Type-Of-Childcare-Training') + '?id=' + application_id)
