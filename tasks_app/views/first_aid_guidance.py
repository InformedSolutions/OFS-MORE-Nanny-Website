from django.shortcuts import render
from django.views import View


class FirstAidGuidanceView(View):
    def get(self, request):
        return render(request, template_name='first-aid-guidance.html')
