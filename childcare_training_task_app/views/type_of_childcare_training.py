from django.views.generic import FormView

from childcare_training_task_app.forms import TypeOfChildcareTrainingForm


class TypeOfChildcareTrainingFormView(FormView):
    """
    Class containing the methods for handling requests to the 'Type-Of-Childcare-Training' page.
    """
    template_name = 'type-of-childcare-training.html'
    form_class = TypeOfChildcareTrainingForm


# from django.shortcuts import render
# from django.views import View
#
#
# class TypeOfChildcareTrainingFormView(View):
#     def get(self, request):
#         return render(request, template_name='type-of-childcare-training.html')
