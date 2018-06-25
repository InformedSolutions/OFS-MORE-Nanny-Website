from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View


from nanny_models.nanny_application import NannyApplication


class ChildcareTrainingGuidanceView(View):
    """
    Class containing the methods for handling requests to the 'Childcare-Training-Guidance' page.
    """
    def get(self, request):
        context = {'id': request.GET['id']}
        return render(request, template_name='childcare-training-guidance.html', context=context)

    def post(self, request):
        application_id = request.GET['id']
        record = NannyApplication.api.get_record(application_id=application_id).record
        record['childcare_training_status'] = "IN_PROGRESS"
        NannyApplication.api.put(record=record)
        return HttpResponseRedirect(reverse('Type-Of-Childcare-Training') + '?id=' + application_id)
