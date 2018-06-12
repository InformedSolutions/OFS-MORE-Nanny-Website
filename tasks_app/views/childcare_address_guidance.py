from django.shortcuts import render
from django.views import View


class ChildcareAddressGuidanceView(View):
    def get(self, request):
        return render(request, template_name='childcare-address-guidance.html')
