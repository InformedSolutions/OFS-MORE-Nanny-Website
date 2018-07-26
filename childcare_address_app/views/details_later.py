from .base import BaseTemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect

from nanny_gateway import NannyGatewayActions


class AddressDetailsLaterView(BaseTemplateView):
    """
    Class containing the view(s) for handling the GET requests to the details later page.
    """

    template_name = 'details-later.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = self.request.GET['id']
        return context

    def post(self, request):
        app_id = request.POST['id']
        # update the task status to be done
        record = NannyGatewayActions().read('application', params={'application_id': app_id})
        record['childcare_address_status'] = 'COMPLETED'
        NannyGatewayActions().put('application', params=record)
        return HttpResponseRedirect(reverse('Task-List') + "?id=" + app_id)
