from .base import BaseTemplateView
from ..utils import *


class CostsView(BaseTemplateView):
    template_name = 'costs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        context['id'] = app_id

        # TODO: re-direct to various confirmation pages as they are built rather than just task list
        context['return_url'] = build_url('Task-List', get={'id': app_id})
        return context

