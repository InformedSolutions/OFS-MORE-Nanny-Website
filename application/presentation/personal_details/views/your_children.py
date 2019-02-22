from application.presentation.base_views import NannyFormView
from application.presentation.utilities import app_id_finder
from application.services.db_gateways import NannyGatewayActions
from ..forms.your_children import PersonalDetailsYourChildrenForm  # Create form with this name


class PersonalDetailsYourChildrenView(NannyFormView):
    template_name = 'your_children.html'
    form_class = PersonalDetailsYourChildrenForm
    success_url = 'personal-details:Personal-Details-Summary'

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
            initial['known_to_social_services'] = personal_details_record['known_to_social_services']
            initial['reasons_known_to_social_services'] = personal_details_record['reasons_known_to_social_services']

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        application_id = app_id_finder(self.request)
        context['id'] = application_id
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        context['personal_details_status'] = application_record['personal_details_status']
        return context

    def form_valid(self, form):
        application_id = app_id_finder(self.request)
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        applicant_personal_details_response = NannyGatewayActions().read('applicant-personal-details', params={
            'application_id': application_id})

        if applicant_personal_details_response.status_code != 200:
            raise ValueError('applicant-personal-details returned a {0} response.'.format(
                applicant_personal_details_response.status_code))

        if application_record['personal_details_status'] not in ['COMPLETED', 'FLAGGED']:
            application_record['personal_details_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=application_record)

        known_to_social_services = form.cleaned_data.get('known_to_social_services', None)
        reasons_known_to_social_services = form.cleaned_data.get('reasons_known_to_social_services', '')

        if known_to_social_services is None:
            raise ValueError('known_to_social_services is a required field, but is None.')
        elif known_to_social_services is True and reasons_known_to_social_services == '':
            raise ValueError('reasons_known_to_social_services cannot be empty if known_to_social_services is True')

        data_dict = {
            'application_id': application_id,
            'known_to_social_services': known_to_social_services,
            'reasons_known_to_social_services': reasons_known_to_social_services,
        }

        patch_response = NannyGatewayActions().patch('applicant-personal-details', params=data_dict)

        if patch_response.status_code != 200:
            raise ValueError(
                "applicant-personal-details patch returned a non 200 response, {0}.".format(patch_response.status_code))

        return super().form_valid(form)
