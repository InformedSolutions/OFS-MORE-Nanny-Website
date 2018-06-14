from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from identity_models.user_details import UserDetails

from middleware import CustomAuthenticationHandler

from login_app.utils import build_url


class ContactDetailsSummaryView(View):
    def get(self, request):
        return render(request, template_name='contact-details-summary.html', context=self.get_user_details_record(request))

    def post(self, request):
        user_details_record = self.get_user_details_record(request)
        response = HttpResponseRedirect(build_url('Task-List', get={'id': user_details_record['application_id']}))

        COOKIE_IDENTIFIER = CustomAuthenticationHandler.get_cookie_identifier()
        if COOKIE_IDENTIFIER not in request.COOKIES:
            CustomAuthenticationHandler.create_session(response, user_details_record['email'])

        return response

    def get_user_details_record(self, request):
        # Depending if the user is coming from task-list or sign-in page.
        try:
            user_details_record = UserDetails.api.get_record(application_id=request.GET['id']).record
        except MultiValueDictKeyError:
            user_details_record = UserDetails.api.get_record(email=request.GET['email_address']).record

        return user_details_record