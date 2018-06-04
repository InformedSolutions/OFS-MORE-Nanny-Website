from django.views import View
from django.shortcuts import render


class ApplicationSavedView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Application-Saved' page.
    """
    def get(self, request):
        return render(request, 'application-saved.html')
