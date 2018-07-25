from .BASE import BaseFormView
from ..forms.lived_abroad import PersonalDetailsLivedAbroadForm

from ..utils import app_id_finder

from nanny_gateway import NannyGatewayActions


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
        personal_details_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
        initial['lived_abroad'] = personal_details_record['lived_abroad']

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = app_id_finder(self.request)
        return context

    def form_valid(self, form):

        application_id = app_id_finder(self.request)
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id})
        application_record['personal_details_status'] = 'IN_PROGRESS'
        NannyGatewayActions().patch('application', params=application_record)

        data_dict = {
            'application_id': application_id,
            'lived_abroad': form.cleaned_data['lived_abroad'],
        }

        NannyGatewayActions().patch('applicant-personal-details', params=data_dict)

        if form.cleaned_data['lived_abroad'] == 'True':
            self.success_url = 'personal-details:Personal-Details-Certificates-Of-Good-Conduct'
        elif form.cleaned_data['lived_abroad'] == 'False':
            self.success_url = 'personal-details:Personal-Details-Summary'

        return super().form_valid(form)
