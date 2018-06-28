from nanny_models.nanny_application import NannyApplication
from nanny_models.dbs_check import DbsCheck

from first_aid_app.views.base import BaseFormView
from dbs_app.forms.dbs_details import DBSDetailsForm
from utils import app_id_finder


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
            response = DbsCheck.api.get_record(application_id=application_id)
            if response.status_code == 200:
                dbs_record = DbsCheck.api.get_record(application_id=application_id).record
            elif response.status_code == 404:
                return initial
        except TypeError:
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
        application_record = NannyApplication.api.get_record(application_id=application_id).record
        application_record['criminal_record_check_status'] = 'IN_PROGRESS'
        NannyApplication.api.put(application_record)

        # Define a dictionary of the data that will potentially be sent to the api
        data_dict = {
            'application_id': application_id,
            'dbs_number': form.cleaned_data['dbs_number'],
            'convictions': form.cleaned_data['convictions'],
        }

        existing_record = DbsCheck.api.get_record(application_id=application_id)
        if existing_record.status_code == 200:
            # Should the record exist, remove application id from the data to be sent (as we don't want any mismatch)
            # and put the record onto the database
            del data_dict['application_id']
            DbsCheck.api.put({**existing_record.record, **data_dict})
        elif existing_record.status_code == 404:
            # Should the record not exist, create it
            DbsCheck.api.create(**data_dict, model_type=DbsCheck)

        # If application has previous cautions or convictions, they must be prompted to send Ofsted their certificate
        if data_dict['convictions'] == 'True':
            self.success_url = 'dbs:DBS-Upload'
        else:
            self.success_url = 'dbs:Summary'

        return super().form_valid(form)
