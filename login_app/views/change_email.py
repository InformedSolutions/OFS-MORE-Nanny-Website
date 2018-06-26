from django.views.generic import TemplateView


class ChangeEmailTemplateView(TemplateView):
    """
    View for handling requests to 'Change-Email' placeholder page.
    """
    template_name = 'change-email.html'
