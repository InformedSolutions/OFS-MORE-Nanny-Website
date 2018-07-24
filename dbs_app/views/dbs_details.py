from nanny_gateway import NannyGatewayActions

from first_aid_app.views.base import BaseFormView
from dbs_app.forms.dbs_details import DBSDetailsForm
from nanny.utilities import app_id_finder


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

        try:
            dbs_record = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
            initial['dbs_number'] = dbs_record['dbs_number']
            initial['convictions'] = dbs_record['convictions']
        except Exception as e:
            if e.error.title == '404 Not Found':
                pass
            else:
                raise e

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

        application_record = NannyGatewayActions().read('application', params={'application_id': application_id})
        application_record['criminal_record_check_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=application_record)

        # Define a dictionary of the data that will potentially be sent to the api
        data_dict = {
            'application_id': application_id,
            'dbs_number': form.cleaned_data['dbs_number'],
            'convictions': form.cleaned_data['convictions'],
        }

        try:
            NannyGatewayActions().put('dbs-check', params=data_dict)
        except Exception as e:
            if e.error.title == '404 Not Found':
                NannyGatewayActions().create('dbs-check', params=data_dict)
            else:
                raise e

        # If application has previous cautions or convictions, they must be prompted to send Ofsted their certificate
        if data_dict['convictions'] == 'True':
            self.success_url = 'dbs:DBS-Upload'
        else:
            self.success_url = 'dbs:Summary'

        return super().form_valid(form)
