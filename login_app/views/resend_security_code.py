from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View


class ResendSecurityCodeView(View):
    """
    Class handling requests to 'Resend-Security-Code' page.
    """
    def get(self, request):
        return render(request, template_name='resend-security-code.html')

    def post(self, request):
        return HttpResponseRedirect(reverse('Security-Code'))
