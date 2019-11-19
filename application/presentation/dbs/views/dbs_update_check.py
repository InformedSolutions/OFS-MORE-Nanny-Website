from application.presentation.base_views import NannyTemplateView
from django.http import HttpResponseRedirect

from ...utilities import app_id_finder, build_url, NO_ADDITIONAL_CERTIFICATE_INFORMATION
from application.services.db_gateways import NannyGatewayActions


class DBSUpdateCheckView(NannyTemplateView):
    """
    Template view to render the DBS update-check page.
    """
    template_name = 'dbs-update-check.html'
    success_url_name = ('dbs:Post-DBS-Certificate', 'dbs:Criminal-Record-Check-Summary-View')

    def get_context_data(self, **kwargs):
        """
        On a post request, set the task status to completed and redirect the user to the task list
        :return:
        """
git         post_dbs, summary = self.success_url_name
        application_id = app_id_finder(self.request)
        crc_response = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
        if crc_response.status_code == 200:
            capita = crc_response.record['is_ofsted_dbs']
            no_information = crc_response.record['certificate_information'] in NO_ADDITIONAL_CERTIFICATE_INFORMATION
            if capita and no_information:
                self.success_url_name = summary
            else:
                self.success_url_name = post_dbs
        else:
            self.success_url_name = summary

        context = super(DBSUpdateCheckView, self).get_context_data(**kwargs)
        return context
