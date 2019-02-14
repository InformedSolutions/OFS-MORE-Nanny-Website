from application.presentation.base_views import NannyTemplateView


class DBSUpdateCheckView(NannyTemplateView):
    """
    Template view to render the DBS update-check page.
    """
    template_name = 'dbs-update-check.html'
    success_url_name = 'dbs:Post-DBS-Certificate'
