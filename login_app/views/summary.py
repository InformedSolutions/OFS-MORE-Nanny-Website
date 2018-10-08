from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render

from nanny.utilities import build_url

from nanny.db_gateways import IdentityGatewayActions, NannyGatewayActions


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
        """ Handle POST request. Create session for user if one not currently existing.
            Redirect to next task to force user to enter personal details before viewing Task list"""

        application_id = request.GET['id']
        api_response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})

        if api_response.status_code == 404:
            response = HttpResponseRedirect(build_url('personal-details:Personal-Details-Name', get={'id': application_id}))
            return response

        else:
            response = HttpResponseRedirect(build_url('Task-List', get={'id': application_id}))
            return response

    def include_change_links(self, application_id):
        """ If the applicant is coming from task list, an application object will exist => get_record gives 200 code."""
        nanny_api_response = NannyGatewayActions().read('application', params={'application_id': application_id})
        return nanny_api_response.status_code == 200
