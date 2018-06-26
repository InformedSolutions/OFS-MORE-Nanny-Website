from django.shortcuts import render
from .base import BaseTemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from nanny_models.nanny_application import *


class AddressDetailsLaterView(BaseTemplateView):
    """
    Class containing the view(s) for handling the GET requests to the details later page.
    """

    template_name = 'details-later.html'

    def post(self, request):
        app_id = request.POST['id']
        # update the task status to be done
        api_response = NannyApplication.api.get_record(
            application_id=app_id
        )
        api_response.record['childcare_address_status'] = 'COMPLETED'
        NannyApplication.api.put(api_response.record)
        return HttpResponseRedirect(reverse('Task-List') + "?id=" + app_id)
