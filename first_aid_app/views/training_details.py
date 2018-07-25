import datetime

from first_aid_app.views.base import BaseFormView
from first_aid_app.forms.training_details import FirstAidTrainingDetailsForm

from nanny_gateway import NannyGatewayActions

from nanny.utilities import app_id_finder


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
            first_aid_record = NannyGatewayActions().read('first_aid_training', params={'application_id': application_id})
            initial['first_aid_training_organisation'] = first_aid_record['training_organisation']
            initial['title_of_training_course'] = first_aid_record['course_title']
            initial['course_date'] = datetime.datetime.strptime(first_aid_record['course_date'], '%Y-%m-%d')
        except Exception as e:
            if e.error.title == '404 Not Found':
                pass
            else:
                raise e

        return initial

    def form_valid(self, form):

        application_id = app_id_finder(self.request)

        application_record = NannyGatewayActions().read('application', {'application_id': application_id})
        application_record['first_aid_training_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=application_record)

        data_dict = {
            'application_id': application_id,
            'training_organisation': form.cleaned_data['first_aid_training_organisation'],
            'course_title': form.cleaned_data['title_of_training_course'],
            'course_date': form.cleaned_data['course_date'].strftime('%Y-%m-%d'),
        }

        try:
            NannyGatewayActions().put('first_aid_training', params=data_dict)
        except Exception as e:
            if e.error.title == '404 Not Found':
                NannyGatewayActions().create('first_aid_training', params=data_dict)
            else:
                raise e

        return super().form_valid(form)
