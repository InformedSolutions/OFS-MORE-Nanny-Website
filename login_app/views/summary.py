from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, reverse

from identity_models.user_details import UserDetails


class ContactDetailsSummaryView(View):
    def get(self, request):
        user_details_record = UserDetails.api.get_record(email=request.GET['email_address']).record
        return render(request, template_name='contact-details-summary.html', context=user_details_record)

    def post(self, request):
        return HttpResponseRedirect(reverse('Task-List') + '/?email_address=' + request.GET['email_address'])
