import datetime

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ImproperlyConfigured

from ..forms.training_details import FirstAidTrainingDetailsForm

from application.presentation.utilities import app_id_finder, build_url
from application.presentation.base_views import NannyFormView
from application.services.db_gateways import NannyGatewayActions


class FirstAidDetailsView(NannyFormView):

    template_name = 'training_details.html'
    form_class = FirstAidTrainingDetailsForm

    def get_initial(self):
        """
        Get initial defines the initial data for the form instance that is to be rendered on the page
        :return: a dictionary mapping form field names, to values of the correct type
        """
        initial = super().get_initial()

        application_id = app_id_finder(self.request)

        response = NannyGatewayActions().read('first-aid', params={'application_id': application_id})
        if response.status_code == 200:
            first_aid_record = response.record
        else:
            return initial

        initial['training_organisation'] = first_aid_record['training_organisation']
        initial['course_title'] = first_aid_record['course_title']
        initial['course_date'] = datetime.datetime.strptime(first_aid_record['course_date'], '%Y-%m-%d')
        # If there has yet to be an entry for the model associated with the form, then no population necessary

        return initial

    def form_valid(self, form):

        application_id = app_id_finder(self.request)
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        application_record['first_aid_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=application_record)

        data_dict = {
            'application_id': application_id,
            'training_organisation': form.cleaned_data['training_organisation'],
            'course_title': form.cleaned_data['course_title'],
            'course_date': form.cleaned_data['course_date'],
        }

        existing_record = NannyGatewayActions().read('first-aid', params={'application_id': application_id})
        if existing_record.status_code == 200:
            NannyGatewayActions().patch('first-aid', params=data_dict)
        elif existing_record.status_code == 404:
            NannyGatewayActions().create('first-aid', params=data_dict)

        if self.__first_aid_renew(form):
            self.success_url = "first-aid:First-Aid-Renew"
        else:
            self.success_url = "first-aid:First-Aid-Declaration"

        return super().form_valid(form)


    def __first_aid_renew(self, form):
        """
        function to determine if first aid course within 2.5 years
        :param form:
        :return:
        """
        renew = False
        today = datetime.date.today()
        course_date = form.cleaned_data['course_date']

        if today - relativedelta(months=30) >= course_date:
            renew = True

        return renew
