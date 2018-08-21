from nanny.base_views import BaseTemplateView


class DeclarationGuidance(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "declaration-guidance.html"
    success_url_name = 'declaration:Declaration-Summary'
