from ..forms.your_children import PersonalDetailsYourChildrenForm # Create form with this name

from nanny.base_views import NannyFormView
from nanny.db_gateways import NannyGatewayActions
from nanny.utilities import app_id_finder


class PersonalDetailsYourChildrenView(NannyFormView):
    template_name = 'your_children.html'
    form_class = PersonalDetailsYourChildrenForm
    success_url = 'Personal-Details-Summary' # Add to url file

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

        initial['child_under16'] = personal_details_record['child_under16'] # Use this name for the form too

        # If there has yet to be an entry for the model associated with the form, then no population necessary

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
        if application_record['personal_details_status'] != 'COMPLETED' or application_record['personal_details_status'] != 'FLAGGED':
            application_record['personal_details_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=application_record)

        data_dict = {
            'application_id': application_id,
            'child_under16': form.cleaned_data['child_under16'],
        }

        existing_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
        if existing_record.status_code == 200:
            NannyGatewayActions().patch('applicant-personal-details', params=data_dict)
        elif existing_record.status_code == 404:
            NannyGatewayActions().create('applicant-personal-details', params=data_dict)

        if form.cleaned_data['child_under16'] == 'True':
            self.success_url = 'personal-details:Personal-Details-Certificates-Of-Good-Conduct'
        elif form.cleaned_data['child_under16'] == 'False':
            self.success_url = 'personal-details:Personal-Details-Summary'

        return super().form_valid(form)
