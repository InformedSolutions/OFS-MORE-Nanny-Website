from django.views import View
from django.shortcuts import render


class CheckEmailView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Check-Email' page.
    """
    def get(self, request):
        email_address = request.GET['email_address']
        return render(request, 'check-email.html', context={'email_address': email_address})
