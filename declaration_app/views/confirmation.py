from nanny.base_views import BaseTemplateView
from nanny.utilities import *
from nanny_models.applicant_personal_details import *


class Confirmation(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "confirmation.html"

    def get_context_data(self, **kwargs):
        app_id = app_id_finder(self.request)
        context = {}
        api_pd_response = ApplicantPersonalDetails.api.get_record(
            application_id=app_id
        )
        if api_pd_response.status_code == 200:
            record = api_pd_response.record
            context['lived_abroad'] = record['lived_abroad']

        api_app_response = NannyApplication.api.get_record(
            application_id=app_id
        )
        if api_app_response.status_code == 200:
            record = api_app_response.record
            context['application_reference'] = record['application_reference']

        context['id'] = app_id
        return context
