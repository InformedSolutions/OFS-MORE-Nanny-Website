from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, reverse

from identity_models.user_details import UserDetails


class ContactDetailsSummaryView(View):
    def get(self, request):
        # Depending if the user is coming from task-list or sign-in page.
        try:
            user_details_record = UserDetails.api.get_record(application_id=request.GET['id']).record
        except:
            user_details_record = UserDetails.api.get_record(application_id=request.GET['id']).record
        return render(request, template_name='contact-details-summary.html', context=user_details_record)

    def post(self, request):
        return HttpResponseRedirect(reverse('Task-List') + '?id=' + request.GET['id'])
