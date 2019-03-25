from application.presentation.base_views import NannyTemplateView


class RenewFirstAid(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "renew-first-aid.html"
    success_url_name = 'first-aid:First-Aid-Summary'


