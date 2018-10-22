from nanny.base_views import NannyTemplateView


class CriminalRecordsCheckGuidanceView(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = 'criminal-record-checks-guidance.html'
    success_url_name = 'dbs:Lived-Abroad-View'
