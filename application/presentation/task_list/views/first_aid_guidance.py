from application.presentation.first_aid.views import NannyTemplateView


class FirstAidGuidanceView(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "first-aid-guidance.html"
    success_url_name = 'first-aid:Training-Details'
