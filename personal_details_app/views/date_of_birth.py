import datetime

from .BASE import BaseFormView
from ..forms.date_of_birth import PersonalDetailsDOBForm

from ..utils import app_id_finder

from nanny.db_gateways import NannyGatewayActions


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

        response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
        if response.status_code == 200:
            personal_details_record = response.record
        elif response.status_code == 404:
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
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        application_record['personal_details_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=application_record)

        data_dict = {
            'application_id': application_id,
            'date_of_birth': form.cleaned_data['date_of_birth'],
        }

        response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
        if response.status_code == 200:
            NannyGatewayActions().patch('applicant-personal-details', params=data_dict)
        elif response.status_code == 404:
            NannyGatewayActions().create('applicant-personal-details', params=data_dict)

        return super().form_valid(form)
