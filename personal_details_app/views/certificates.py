from nanny.base_views import NannyTemplateView


class PersonalDetailCertificateView(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "certificates_of_good_conduct.html"
    success_url_name = 'personal-details:Personal-Details-Post-Certificates'


class PersonalDetailsPostCertificateView(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "send_certificates.html"
    success_url_name = 'personal-details:Personal-Details-Your-Children'
