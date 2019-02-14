from application.services.db_gateways import NannyGatewayActions
from application.presentation.base_views import NannyFormView
from application.presentation.utilities import app_id_finder
from ..forms.dbs_details import CaptiaDBSDetailsForm
from application.services.dbs import read_dbs, dbs_within_three_months

NO_ADDITIONAL_CERTIFICATE_INFORMATION = ['Certificate contains no information']

class CapitaDBSDetailsFormView(NannyFormView):
    template_name = 'capita-dbs-details.html'
    form_class = CaptiaDBSDetailsForm
    success_url = None

    def form_valid(self, form):
        application_id = self.request.GET['id']
        criminal_checks_record = {'application_id': application_id}
        dbs_number = form.cleaned_data['dbs_number']
        response = read_dbs(dbs_number)
        if response.status_code == 200:
            dbs_record = getattr(read_dbs(dbs_number), 'record', None)
            if dbs_record is not None:
                info = dbs_record['certificate_information']
                if dbs_within_three_months(dbs_record):
                    if not info in NO_ADDITIONAL_CERTIFICATE_INFORMATION:
                        self.success_url = 'dbs:Criminal-Record-Check-Summary-View'
                    else:
                        self.success_url = 'dbs:Post-DBS-Certificate'
                    criminal_checks_record['within_three_months'] = True
                else:
                    self.success_url = 'dbs:DBS-Type-View'
                    criminal_checks_record['within_three_months'] = False
                criminal_checks_record['dbs_number'] = dbs_number
                criminal_checks_record['is_ofsted_dbs'] = True
                criminal_checks_record['certificate_information'] = info
        else:
            self.success_url = 'dbs:DBS-Type-View'
            criminal_checks_record['dbs_number'] = dbs_number
            criminal_checks_record['is_ofsted_dbs'] = False

        NannyGatewayActions().put('dbs-check', params=criminal_checks_record)

        return super(CapitaDBSDetailsFormView, self).form_valid(form)

    def get_initial(self):
        """
        Get initial defines the initial data for the form instance that is to be rendered on the page
        :return: a dictionary mapping form field names, to values of the correct type
        """
        initial = super().get_initial()

        application_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
        dbs_record = api_response.record
        initial['dbs_number'] = dbs_record['dbs_number']
        initial['convictions'] = dbs_record['convictions']
        initial['application_id'] = application_id
        return initial
