from .BASE import BaseTemplateView
from ..utils import app_id_finder


class PersonalDetailCertificateView(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "certificates_of_good_conduct.html"
    success_url_name = 'personal-details:Personal-Details-Post-Certificates'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = app_id_finder(self.request)
        return context


class PersonalDetailsPostCertificateView(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "send_certificates.html"
    success_url_name = 'personal-details:Personal-Details-Summary'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = app_id_finder(self.request)
        return context