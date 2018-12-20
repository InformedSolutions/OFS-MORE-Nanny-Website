from nanny.base_views import NannyTemplateView


class EmailGoodConductCertificatesView(NannyTemplateView):
    """
    Template view to render the Email Certificates of Good Conduct page.
    """
    template_name = 'email-good-conduct-certificates.html'
    success_url_name = 'dbs:DBS-Guidance-View'
