from nanny.base_views import NannyTemplateView


class InsuranceCoverView(NannyTemplateView):
    template_name = 'insurance-cover.html'
    success_url_name = 'insurance:Summary'
