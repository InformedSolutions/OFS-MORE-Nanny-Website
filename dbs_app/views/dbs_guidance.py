from first_aid_app.views.base import BaseTemplateView


class DBSGuidance(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "dbs-guidance.html"
    success_url_name = 'dbs:Details'
