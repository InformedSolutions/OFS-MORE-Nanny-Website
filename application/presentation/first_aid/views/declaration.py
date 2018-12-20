from nanny.base_views import NannyTemplateView


class Declaration(NannyTemplateView):
    """
    Template view to  render the declaration page from first access of task from task list
    """
    template_name = "declaration.html"
    success_url_name = 'first-aid:First-Aid-Summary'
