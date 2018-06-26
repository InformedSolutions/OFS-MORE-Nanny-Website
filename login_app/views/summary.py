from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render

from identity_models.user_details import UserDetails

from nanny_models.nanny_application import NannyApplication

from middleware import CustomAuthenticationHandler

from login_app.utils import build_url


class ContactDetailsSummaryView(View):
    def get(self, request):
        application_id = request.GET['id']
        context = self.get_user_details_record(application_id)
        context['include_change_links'] = self.include_change_links(application_id)
        context['application_id'] = application_id
        return render(request, template_name='contact-details-summary.html', context=context)

    def post(self, request):
        application_id = request.GET['id']
        user_details_record = self.get_user_details_record(application_id)
        response = HttpResponseRedirect(build_url('Task-List', get={'id': application_id}))

        COOKIE_IDENTIFIER = CustomAuthenticationHandler.get_cookie_identifier()
        if COOKIE_IDENTIFIER not in request.COOKIES:
            CustomAuthenticationHandler.create_session(response, user_details_record['email'])

        return response

    def get_user_details_record(self, application_id):
        return UserDetails.api.get_record(application_id=application_id).record

    def include_change_links(self, application_id):
        """ If the applicant is coming from task list, an application object will exist => get_record gives 200 code."""
        nanny_api_response = NannyApplication.api.get_record(application_id=application_id)
        # return True if nanny_api_response.status_code == 200 else False
        return nanny_api_response.status_code == 200
