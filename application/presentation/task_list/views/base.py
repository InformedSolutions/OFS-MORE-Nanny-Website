from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import render


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(**kwargs)
        app_id = self.request.GET.get('id')
        context['application_id'] = app_id
        return context


class ServiceUnavailableView(View):
    """
    Class containing the view(s) for handling the GET requests to the 'Service-Unavailable' page.
    """
    def get(self, request):
        return render(request, 'service-unavailable.html')