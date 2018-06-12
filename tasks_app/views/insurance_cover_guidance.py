from django.shortcuts import render
from django.views import View


class InsuranceCoverGuidanceView(View):
    def get(self, request):
        return render(request, template_name='insurance-cover-guidance.html')
