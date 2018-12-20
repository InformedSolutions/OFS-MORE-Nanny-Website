from nanny.base_views import NannyTemplateView


class DeclarationGuidance(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "declaration-guidance.html"
    success_url_name = 'declaration:Declaration-Summary'
