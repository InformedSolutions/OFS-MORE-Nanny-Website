from nanny.base_views import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from nanny.utilities import *
from nanny_models.insurance_cover import *

class SummaryView(BaseTemplateView):
    template_name = 'insurance-summary.html'
    success_url_name = 'Task-List'

    def get_context_data(self):
        context = super().get_context_data()
        app_id = context['id']
        api_response = InsuranceCover.api.get_record(application_id=app_id)
        if api_response.status_code == 200:
            public_liability = api_response.record['public_liability']
            if public_liability:
                context['public_liability'] = 'Yes'
            else:
                context['public_liability'] = 'No'

        return context

    def post(self, request):
        app_id = app_id_finder(self.request)
        # update task status to be done
        app_api_response = NannyApplication.api.get_record(application_id=app_id)
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['insurance_cover_status'] = 'COMPLETED'
            NannyApplication.api.put(record)

        return HttpResponseRedirect(build_url('Task-List', get={'id': app_id}))