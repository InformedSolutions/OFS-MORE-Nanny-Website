from nanny.base_views import *
from nanny.utilities import *
from ..forms.public_liability import PublicLiabilityForm
from nanny_models.insurance_cover import *


class PublicLiabilityView(NannyFormView):
    template_name = 'public-liability.html'
    success_url = ''
    form_class = PublicLiabilityForm

    def get_initial(self):
        initial = super().get_initial()
        app_id = app_id_finder(self.request)

        api_response = InsuranceCover.api.get_record(application_id=app_id)
        if api_response.status_code == 200:
            initial['public_liability'] = api_response.record['public_liability']

        return initial

    def form_valid(self, form):
        app_id = app_id_finder(self.request)
        public_liability = form.cleaned_data['public_liability']
        api_response = InsuranceCover.api.get_record(application_id=app_id)

        if api_response.status_code == 200:
            record = api_response.record
            record['public_liability'] = public_liability
            InsuranceCover.api.put(record)

        elif api_response.status_code == 404:
            InsuranceCover.api.create(
                application_id=app_id,
                public_liability=public_liability,
                model_type=InsuranceCover
            )

        if public_liability == 'True':
            self.success_url = 'insurance:Summary'
        elif public_liability == 'False':
            self.success_url = 'insurance:Insurance-Cover'

        # set status of insurance cover task to 'in progress'
        app_api_response = NannyApplication.api.get_record(application_id=app_id)
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['insurance_cover_status'] = 'IN_PROGRESS'
            NannyApplication.api.put(record)

        return super(PublicLiabilityView, self).form_valid(form)
