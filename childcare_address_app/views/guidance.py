from django.shortcuts import render
from .base import BaseTemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from nanny_models.nanny_application import *
from nanny_models.childcare_address import *


class GuidanceView(BaseTemplateView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address guidance page.
    """

    template_name = 'childcare-address-guidance.html'
    success_url = 'Childcare-Address-Where-You-Work'

    def get(self, request, *args, **kwargs):
        """
        Handle get requests to the guidance page.
        """
        app_id = request.GET['id']
        api_response = ChildcareAddress.api.get_records(
            application_id=app_id
        )

        # if there are any existing childcare address records, reroute the user to the address details page
        # to prevent them from being able to add more than five addresses.
        if api_response.status_code != 404:
            return HttpResponseRedirect(reverse('Childcare-Address-Details') + "?id=" + app_id)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request):
        """
        Handle post requests to the guidance page.
        """
        app_id = request.POST['id']

        # update the task status to be in progress
        api_response = NannyApplication.api.get_record(
            application_id=app_id
        )
        api_response.record['childcare_address_status'] = 'IN_PROGRESS'
        NannyApplication.api.put(api_response.record)

        return HttpResponseRedirect(reverse('Childcare-Address-Where-You-Work') + "?id=" + app_id)

