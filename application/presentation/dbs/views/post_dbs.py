from application.presentation.base_views import NannyTemplateView


class PostDBSCertificateView(NannyTemplateView):
    """
    Template view to render the 'post your DBS certificate' page.
    """
    template_name = 'post-dbs-certificate.html'
    success_url_name = 'dbs:Criminal-Record-Check-Summary-View'
