from django.shortcuts import HttpResponseRedirect, render, reverse
from django.views.generic import TemplateView, View

from nanny.db_gateways import NannyGatewayActions, IdentityGatewayActions
from nanny.middleware import CustomAuthenticationHandler


class CancelApplicationTemplateView(View):
    """
    Class containing the methods for handling requests to the 'Cancel-Application' page.
    """
    def get(self, request):
        application_id = request.GET['id']
        return render(request, template_name='cancel-application.html', context={'id': application_id})

    def post(self, request):
        application_id = request.GET['id']

        # Delete user information.
        NannyGatewayActions().delete('application', params={'application_id': application_id})
        IdentityGatewayActions().delete('user', params={'application_id': application_id})

        # Destroy session.
        response = HttpResponseRedirect(reverse('Application-Cancelled'))
        CustomAuthenticationHandler.destroy_session(response)
        return response


class ApplicationCancelledTemplateView (TemplateView):
    """
    Class containing the methods for handling GET requests to the 'Application-Cancelled' page.
    """
    template_name = 'application-cancelled.html'
