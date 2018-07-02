from nanny.base_views import *


class GuidanceView(BaseTemplateView):
    template_name = 'insurance-guidance.html'
    success_url_name = 'insurance:Public-Liability'
