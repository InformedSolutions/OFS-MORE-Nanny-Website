from django.shortcuts import render
from django.views import View


class CriminalRecordGuidanceView(View):
    def get(self, request):
        return render(request, template_name='criminal-record-guidance.html')
