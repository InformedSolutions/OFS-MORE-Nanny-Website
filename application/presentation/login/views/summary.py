import datetime

from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render

from application.presentation.utilities import build_url

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


class ContactDetailsSummaryView(View):
    """
    Class for handling requests to the 'Contact-Details-Summary' page.
    """
    def get(self, request):
        """ Handle GET request. Pass user details record, app_id and Bool for including change links to template
            as context."""
        application_id = request.GET['id']
        context = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
        context['include_change_links'] = self.include_change_links(application_id)
        context['id'] = application_id
        return render(request, template_name='contact-details-summary.html', context=context)

    def post(self, request):
        """ Handle POST request. Create session for user if the request does not return a record. If a record exists,
        a check is completed on if the user has completed the personal details task. If they have, they are presented
        with the task-list, if not they are presented with the personal details task"""

        application_id = request.GET['id']
        nanny_api_response = NannyGatewayActions().read('application', params={'application_id': application_id})

        if nanny_api_response.status_code == 200:
            application_record = NannyGatewayActions().read('application',
                                                            params={'application_id': application_id}).record

            # This differentiates between a new user and one who has signed out during the personal details task.
            if application_record['personal_details_status'] == 'COMPLETED':
                response = HttpResponseRedirect(build_url('Task-List', get={'id': application_id}))
                return response

            else:
                return HttpResponseRedirect(build_url('personal-details:Personal-Details-Name', get={
                    'id': application_id}))

        if nanny_api_response.status_code == 404:
            NannyGatewayActions().create(
                'application',
                params={
                    'application_id': application_id,
                    'application_status': 'DRAFTING',
                    'login_details_status': 'COMPLETED',
                    'date_last_accessed': datetime.datetime.now(),
                }
            )
            return HttpResponseRedirect(build_url('personal-details:Personal-Details-Name', get={
                'id': application_id}))

    def include_change_links(self, application_id):
        """ If the applicant is coming from task list, an application object will exist => get_record gives 200 code."""
        nanny_api_response = NannyGatewayActions().read('application', params={'application_id': application_id})
        return nanny_api_response.status_code == 200
