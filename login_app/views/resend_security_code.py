from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from identity_models.user_details import UserDetails

from login_app.utils import build_url

from .validate_magic_link import ValidateMagicLinkView


class ResendSecurityCodeView(View):
    """
    Class handling requests to 'Resend-Security-Code' page.
    """
    def get(self, request):
        return render(request, template_name='resend-security-code.html')

    def post(self, request):
        get = {'email_address': request.GET['email_address']}

        record = UserDetails.api.get_record(email=get['email_address']).record
        record = ValidateMagicLinkView.sms_magic_link(record=record)
        UserDetails.api.put(record)

        return HttpResponseRedirect(build_url('Security-Code', get=get))
