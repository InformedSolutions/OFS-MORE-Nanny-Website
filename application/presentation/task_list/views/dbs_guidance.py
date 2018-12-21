from application.presentation.base_views import NannyTemplateView


class DBSGuidance(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "dbs-guidance.html"
    success_url_name = 'dbs:Details'
