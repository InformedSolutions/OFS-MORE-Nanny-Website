from django.views import View
from django.shortcuts import render


class StartPageView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Check-Email' page.
    """
    def get(self, request):
        return render(request, 'start-page.html')
