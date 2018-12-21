from application.presentation.base_views import NannyTemplateView


class CriminalRecordsFromAbroadView(NannyTemplateView):
    """
    Template view to render the Get A DBS page.
    """
    template_name = 'criminal-record-abroad.html'
    success_url_name = 'dbs:Email-Good-Conduct-Certificates-View'
