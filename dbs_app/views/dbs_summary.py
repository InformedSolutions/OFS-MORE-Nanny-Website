from django.http import HttpResponseRedirect

from nanny_models.nanny_application import NannyApplication
from nanny_models.dbs_check import DbsCheck

from first_aid_app.views.base import BaseTemplateView, build_url
from utils import app_id_finder


class DBSSummary(BaseTemplateView):
    """
    View to render the DBS summary page and act on post requests accordingly
    """

    template_name = 'dbs-summary.html'
    success_url_name = 'Task-List'

    def post(self):
        """
        On a post request, set the task status to completed and redirect the user to the task list
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
        context = super().get_context_data()
        application_id = app_id_finder(self.request)
        context['link_url'] = build_url(self.success_url_name, get={'id': application_id})
        context['id'] = application_id
        context['dbs_record'] = DbsCheck.api.get_record(application_id=application_id).record
        return context
