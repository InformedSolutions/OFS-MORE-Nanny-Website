from first_aid_app.views.base import BaseTemplateView


class MasterSummary(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "final-declaration.html"
    success_url_name = 'declaration-payment:declaration-guidance'
