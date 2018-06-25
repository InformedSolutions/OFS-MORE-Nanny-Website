import datetime

from nanny_models.nanny_application import NannyApplication

from first_aid_app.views.base import BaseFormView
from first_aid_app.forms.training_details import FirstAidTrainingDetailsForm

from nanny_models.first_aid import FirstAidTraining

from utils import app_id_finder


class FirstAidDetailsView(BaseFormView):

    template_name = 'training_details.html'
    form_class = FirstAidTrainingDetailsForm
    success_url = 'first-aid:First-Aid-Declaration'

    def get_initial(self):
        """
        Get initial defines the initial data for the form instance that is to be rendered on the page
        :return: a dictionary mapping form field names, to values of the correct type
        """
        initial = super().get_initial()

        application_id = app_id_finder(self.request)
        try:
            response = FirstAidTraining.api.get_record(application_id=application_id)
            if response.status_code == 200:
                first_aid_record = FirstAidTraining.api.get_record(application_id=application_id).record
            elif response.status_code == 404:
                return initial
        except TypeError:
            return initial
        initial['first_aid_training_organisation'] = first_aid_record['training_organisation']
        initial['title_of_training_course'] = first_aid_record['course_title']
        initial['course_date'] = datetime.datetime.strptime(first_aid_record['course_date'], '%Y-%m-%d')
        # If there has yet to be an entry for the model associated with the form, then no population necessary

        return initial

    def form_valid(self, form):

        application_id = app_id_finder(self.request)
        application_record = NannyApplication.api.get_record(application_id=application_id).record
        application_record['first_aid_training_status'] = 'IN_PROGRESS'
        NannyApplication.api.put(application_record)

        data_dict = {
            'application_id': application_id,
            'training_organisation': form.cleaned_data['first_aid_training_organisation'],
            'course_title': form.cleaned_data['title_of_training_course'],
            'course_date': form.cleaned_data['course_date'],
        }

        existing_record = FirstAidTraining.api.get_record(application_id=application_id)
        if existing_record.status_code == 200:
            del data_dict['application_id']
            FirstAidTraining.api.put({**existing_record.record, **data_dict})
        elif existing_record.status_code == 404:
            FirstAidTraining.api.create(**data_dict, model_type=FirstAidTraining)

        return super().form_valid(form)
