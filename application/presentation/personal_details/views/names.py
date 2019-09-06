from ..forms.name import PersonalDetailsNameForm
from django.conf import settings

from application.presentation.base_views import NannyFormView
from application.services.db_gateways import NannyGatewayActions
from application.presentation.utilities import app_id_finder


class PersonalDetailNameView(NannyFormView):
    template_name = 'names.html'
    form_class = PersonalDetailsNameForm
    success_url = 'personal-details:Personal-Details-Date-Of-Birth'

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

        if personal_details_record['title'] in settings.TITLE_OPTIONS:
            initial['title'] = personal_details_record['title']
        else:
            initial['title'] = 'Other'
            initial['other_title'] = personal_details_record['title']
        initial['first_name'] = personal_details_record['first_name']
        initial['middle_names'] = personal_details_record['middle_names']
        initial['last_name'] = personal_details_record['last_name']
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

        if form.cleaned_data['title'] != 'Other':
            title = form.cleaned_data['title']
        else:
            title = form.cleaned_data['other_title']

        data_dict = {
            'application_id': application_id,
            'title': title,
            'first_name': form.cleaned_data['first_name'],
            'middle_names': form.cleaned_data['middle_names'],
            'last_name': form.cleaned_data['last_name'],
        }

        existing_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
        if existing_record.status_code == 200:
            NannyGatewayActions().patch('applicant-personal-details', params=data_dict)
        elif existing_record.status_code == 404:
            NannyGatewayActions().create('applicant-personal-details', params=data_dict)

        return super().form_valid(form)
