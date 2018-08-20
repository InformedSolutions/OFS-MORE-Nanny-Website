from first_aid_app.views.base import BaseFormView
from dbs_app.forms.dbs_details import DBSDetailsForm
from nanny.utilities import app_id_finder

from nanny.db_gateways import NannyGatewayActions


class DBSDetailsView(BaseFormView):

    template_name = 'dbs-details.html'
    form_class = DBSDetailsForm
    success_url = 'dbs:DBS-Upload'

    def get_initial(self):
        """
        Get initial defines the initial data for the form instance that is to be rendered on the page
        :return: a dictionary mapping form field names, to values of the correct type
        """
        initial = super().get_initial()

        application_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
        if api_response.status_code == 200:
            dbs_record = api_response.record
        elif api_response.status_code == 404:
            return initial
        initial['dbs_number'] = dbs_record['dbs_number']
        initial['convictions'] = dbs_record['convictions']
        # If there has yet to be an entry for the model associated with the form, then no population necessary

        return initial

    def form_valid(self, form):
        """
        Should the DBS for details be valid, update or create the databse record, set the task status to in progress,
        then decide where to redirect the user base on their answer to the convictions question
        :param form:
        :return:
        """

        # Change the task status to in progress, as data entry marks setting the task status to in progress
        application_id = app_id_finder(self.request)
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        application_record['dbs_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=application_record)

        # Define a dictionary of the data that will potentially be sent to the api
        data_dict = {
            'dbs_number': form.cleaned_data['dbs_number'],
            'convictions': form.cleaned_data['convictions'],
            'application_id': application_id,
        }

        existing_record = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
        if existing_record.status_code == 200:
            NannyGatewayActions().patch('dbs-check', params=data_dict)
        elif existing_record.status_code == 404:
            # Should the record not exist, create it, adding the application id to the data dict
            NannyGatewayActions().create('dbs-check', params=data_dict)

        # If application has previous cautions or convictions, they must be prompted to send Ofsted their certificate
        if data_dict['convictions'] == 'True':
            self.success_url = 'dbs:DBS-Upload'
        else:
            self.success_url = 'dbs:Summary'

        return super().form_valid(form)
