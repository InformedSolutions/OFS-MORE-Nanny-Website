from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from nanny.utilities import build_url

from .validate_magic_link import ValidateMagicLinkView

from db_gateways import IdentityGatewayActions


class ResendSecurityCodeView(View):
    """
    Class handling requests to 'Resend-Security-Code' page.
    """
    def get(self, request):
        application_id = request.GET['id']
        record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record

        # If the applicant has attempted more than 3 attempts in the past 24 hours, redirect to security question.
        if record['sms_resend_attempts'] >= 3:
            return HttpResponseRedirect(build_url('Security-Question', get={'id': application_id}))

        return render(request, template_name='resend-security-code.html')

    def post(self, request):
        application_id = request.GET['id']
        record = IdentityGatewayActions().read('user', params={'application_id': application_id}).record
        record = ValidateMagicLinkView.sms_magic_link(record=record)

        if record['sms_resend_attempts'] is not None:
            record['sms_resend_attempts'] += 1
        else:
            record['sms_resend_attempts'] = 1

        IdentityGatewayActions().put('user', params=record)

        return HttpResponseRedirect(build_url('Security-Code', get={'id': application_id}))
