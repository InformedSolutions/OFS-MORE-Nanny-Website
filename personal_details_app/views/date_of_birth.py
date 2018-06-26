import datetime

from nanny_models.nanny_application import NannyApplication

from .BASE import BaseFormView
from ..forms.date_of_birth import PersonalDetailsDOBForm

from nanny_models.applicant_personal_details import ApplicantPersonalDetails

from ..utils import app_id_finder


class PersonalDetailDOBView(BaseFormView):

    template_name = 'dob.html'
    form_class = PersonalDetailsDOBForm
    success_url = 'personal-details:Personal-Details-Home-Address'

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
        try:
            initial['date_of_birth'] = datetime.datetime.strptime(personal_details_record['date_of_birth'], '%Y-%m-%d')
        except TypeError:
            initial['date_of_birth'] = None

        # If there has yet to be an entry for the model associated with the form, then no population necessary

        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        context['id'] = app_id
        return context

    def form_valid(self, form):

        application_id = app_id_finder(self.request)
        application_record = NannyApplication.api.get_record(application_id=application_id).record
        application_record['personal_details_status'] = 'IN_PROGRESS'
        NannyApplication.api.put(application_record)

        data_dict = {
            'application_id': application_id,
            'date_of_birth': form.cleaned_data['date_of_birth'],
        }

        existing_record = ApplicantPersonalDetails.api.get_record(application_id=application_id)
        if existing_record.status_code == 200:
            del data_dict['application_id']
            ApplicantPersonalDetails.api.put({**existing_record.record, **data_dict})
        elif existing_record.status_code == 404:
            ApplicantPersonalDetails.api.create(**data_dict, model_type=ApplicantPersonalDetails)

        return super().form_valid(form)
