from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from nanny_models.nanny_application import NannyApplication
from nanny_models.dbs_check import DbsCheck

from first_aid_app.views.base import BaseTemplateView, build_url


class DBSSummary(View):
    """
    View to render the DBS summary page and act on post requests accordingly
    """

    template_name = 'dbs-summary.html'
    success_url_name = 'Task-List'

    def get(self, request):

        # Grab the record for rendering on the template and render the page
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        """
        On a post request, set the task status to completed and redirect the user to the task list
        :param request:
        :return:
        """

        application_id = self.request.POST['id']
        application_record = NannyApplication.api.get_record(application_id=application_id).record
        application_record['criminal_record_check_status'] = 'COMPLETED'
        NannyApplication.api.put(application_record)

        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': application_id}))

    def get_context_data(self, **kwargs):
        """
        Grab the redirect url to the task list, the application id, and the full dbs record (render order occurs in
        the template)
        :param kwargs:
        :return:
        """
        context = {}
        application_id = self.request.GET['id']
        context['link_url'] = build_url(self.success_url_name, get={'id': application_id})
        context['id'] = self.request.GET['id']
        context['dbs_record'] = DbsCheck.api.get_record(application_id=application_id).record
        return context