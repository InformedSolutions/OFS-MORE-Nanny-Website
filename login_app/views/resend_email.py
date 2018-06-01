from django.shortcuts import render
from django.views import View


class ResendEmail(View):
    """
    Class containing the methods for handling requests to the 'Resend-Email' page.
    """
    def get(self, request):
        # email_address = request.GET['email_address']
        email_address = 'placeholder_email@add_api.com'  # Have placeholder email until Identify API operational.
        return render(request, template_name='email-resent.html', context={'email_address': email_address})
