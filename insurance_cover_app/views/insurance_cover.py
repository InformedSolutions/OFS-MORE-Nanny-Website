from nanny.base_views import *


class InsuranceCoverView(BaseTemplateView):
    template_name = 'insurance-cover.html'
    success_url_name = 'insurance:Summary'
