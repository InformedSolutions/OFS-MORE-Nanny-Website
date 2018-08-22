from nanny.base_views import NannyTemplateView


class GuidanceView(NannyTemplateView):
    template_name = 'insurance-guidance.html'
    success_url_name = 'insurance:Public-Liability'
