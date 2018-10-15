from nanny.base_views import NannyTemplateView


class YourChildrenGuidance(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "your_children.html"
    success_url_name = 'task-list'
