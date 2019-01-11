from django.views import View
from django.shortcuts import render

from nanny.middleware import CustomAuthenticationHandler


class ApplicationSavedView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Application-Saved' page.
    """
    def get(self, request):
        cookie_key = CustomAuthenticationHandler.get_cookie_identifier()
        request.COOKIES[cookie_key] = None
        response = render(request, 'application-saved.html')
        CustomAuthenticationHandler.destroy_session(response)
        return response
