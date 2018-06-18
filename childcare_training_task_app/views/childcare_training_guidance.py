from django.shortcuts import render
from django.views import View


class ChildcareTrainingGuidanceView(View):
    def get(self, request):
        return render(request, template_name='childcare-training-guidance.html')
