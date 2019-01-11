from application.presentation.base_views import NannyTemplateView


class Guidance(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "guidance.html"
    success_url_name = 'first-aid:Training-Details'
