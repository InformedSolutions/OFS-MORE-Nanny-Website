from application.presentation.base_views import NannyTemplateView


class DBSGuidanceView(NannyTemplateView):
    """
    Template view to render the DBS guidance page.
    """
    template_name = 'dbs-guidance.html'
    success_url_name = 'dbs:Capita-DBS-Details-View'
