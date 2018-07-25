import datetime
from coreapi.exceptions import ErrorMessage

from .BASE import BaseFormView
from ..forms.date_of_birth import PersonalDetailsDOBForm

from nanny_gateway import NannyGatewayActions

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
        personal_details_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})

        if personal_details_record['date_of_birth'] is not None:
            initial['date_of_birth'] = datetime.datetime.strptime(personal_details_record['date_of_birth'], '%Y-%m-%d')

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        context['id'] = app_id
        return context

    def form_valid(self, form):
        application_id = app_id_finder(self.request)
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id})
        application_record['personal_details_status'] = 'IN_PROGRESS'
        NannyGatewayActions().patch('application', params=application_record)

        data_dict = {
            'application_id': application_id,
            'date_of_birth': form.cleaned_data['date_of_birth'].strftime('%Y-%m-%d'),
        }

        try:
            NannyGatewayActions().patch('applicant-personal-details', params=data_dict)
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                NannyGatewayActions().create('applicant-personal-details', params=data_dict)
            else:
                raise e

        return super().form_valid(form)
