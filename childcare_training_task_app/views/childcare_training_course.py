from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View

from nanny_models.application import Application


class ChildcareTrainingCourseView(View):
    def get(self, request):
        application_id = request.GET['id']
        context = {'id': application_id}
        record = Application.api.get_record(application_id=application_id)
        record['childcare_training_status'] = 'IN_PROGRESS'
        Application.api.put(record=record)
        return render(request, template_name='childcare-training-course', context=context)

    def post(self, request):
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + request.GET['id'])
