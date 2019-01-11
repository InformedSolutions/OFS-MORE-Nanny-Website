from django.shortcuts import render
from django.views import View


class PersonalDetailsGuidanceView(View):
    def get(self, request):
        return render(request, template_name='personal-details-guidance.html')
