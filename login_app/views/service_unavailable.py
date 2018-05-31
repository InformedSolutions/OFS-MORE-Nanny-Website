from django.views import View
from django.shortcuts import render


class ServiceUnavailableView(View):
    def get(self, request):
        return render(request, 'service-unavailable.html')
