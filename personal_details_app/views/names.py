from coreapi.exceptions import ErrorMessage

from .BASE import BaseFormView
from ..forms.name import PersonalDetailsNameForm

from nanny_gateway import NannyGatewayActions

from ..utils import app_id_finder


class PersonalDetailNameView(BaseFormView):

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

        try:
            personal_details_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
            initial['first_name'] = personal_details_record['first_name']
            initial['middle_names'] = personal_details_record['middle_names']
            initial['last_name'] = personal_details_record['last_name']
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                pass
            else:
                raise e

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = app_id_finder(self.request)
        return context

    def form_valid(self, form):
        application_id = app_id_finder(self.request)
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id})
        application_record['personal_details_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', application_record)

        data_dict = {
            'application_id': application_id,
            'first_name': form.cleaned_data['first_name'],
            'middle_names': form.cleaned_data['middle_names'],
            'last_name': form.cleaned_data['last_name'],
        }

        try:
            NannyGatewayActions().patch('applicant-personal-details', params=data_dict)
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                NannyGatewayActions().create('applicant-personal-details', params=data_dict)
            else:
                raise e

        return super().form_valid(form)
