from django.views import View
from django.shortcuts import render

from application.services.db_gateways import IdentityGatewayActions

class CheckEmailView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Check-Email' page.
    """
    def get(self, request):
        if request.GET.get('id'):

            application_id = request.GET.get('id')
            user_details = IdentityGatewayActions().read('user', params={'application_id': application_id}).record

            change_email = user_details['change_email']
            email_address = user_details['email']

            if change_email is not None:
                application_id = request.GET.get('id')

                return render(request, 'check-email.html',
                                  context={'email_address': change_email, 'id': application_id})
            else:
                return render(request, 'check-email.html',
                              context={'email_address': email_address})
        else:
            email_address = request.GET.get('email_address')
            return render(request, 'check-email.html',
                          context={'email_address': email_address})
