from django.views import View
from django.shortcuts import render


class ServiceUnavailableView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Service-Unavailable' page.
    """
    def get(self, request):
        return render(request, 'service-unavailable.html')
