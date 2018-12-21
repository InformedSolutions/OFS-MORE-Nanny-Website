from application.presentation.base_views import NannyTemplateView


class RegistrationRules(NannyTemplateView):
    """
    Template view to  render the registration rules from the declaration app
    """
    template_name = "registration-rules.html"
    # To avoid errors due to lack of redirect on page, the 'success_url_name' is the information page itself, but this will never be called anyway due to the lack of form submission
    success_url_name = 'declaration:Registration-Rules'
