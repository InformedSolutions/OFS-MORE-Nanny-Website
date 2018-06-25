import datetime

from nanny_models.nanny_application import NannyApplication
from nanny_models.applicant_personal_details import ApplicantPersonalDetails

from .BASE import BaseFormView
from ..forms.lived_abroad import PersonalDetailsLivedAbroadForm

from ..utils import app_id_finder


class PersonalDetailLivedAbroadView(BaseFormView):

    template_name = 'lived_abroad.html'
    form_class = PersonalDetailsLivedAbroadForm
    success_url = 'task-list'

    def get_initial(self):
        """
        Get initial defines the initial data for the form instance that is to be rendered on the page
        :return: a dictionary mapping form field names, to values of the correct type
        """
        initial = super().get_initial()

        application_id = app_id_finder(self.request)
        try:
            response = ApplicantPersonalDetails.api.get_record(application_id=application_id)
            if response.status_code == 200:
                personal_details_record = ApplicantPersonalDetails.api.get_record(application_id=application_id).record
            elif response.status_code == 404:
                return initial
            print(response.status_code)
        except TypeError:
            return initial

        initial['lived_abroad'] = personal_details_record['lived_abroad']

        # If there has yet to be an entry for the model associated with the form, then no population necessary

        return initial

    def form_valid(self, form):

        application_id = app_id_finder(self.request)
        application_record = NannyApplication.api.get_record(application_id=application_id).record
        application_record['personal_details_status'] = 'IN_PROGRESS'
        NannyApplication.api.put(application_record)

        data_dict = {
            'application_id': application_id,
            'lived_abroad': form.cleaned_data['lived_abroad'],
        }

        existing_record = ApplicantPersonalDetails.api.get_record(application_id=application_id)
        if existing_record.status_code == 200:
            del data_dict['application_id']
            ApplicantPersonalDetails.api.put({**existing_record.record, **data_dict})
        elif existing_record.status_code == 404:
            ApplicantPersonalDetails.api.create(**data_dict, model_type=ApplicantPersonalDetails)

        if form.cleaned_data['lived_abroad'] == 'True':
            self.success_url = 'personal-details:Personal-Details-Certificates-Of-Good-Conduct'
        elif form.cleaned_data['lived_abroad'] == 'False':
            self.success_url = 'personal-details:Personal-Details-Summary'

        return super().form_valid(form)
