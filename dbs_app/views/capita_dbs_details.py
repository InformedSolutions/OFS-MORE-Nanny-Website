from nanny.db_gateways import NannyGatewayActions
from nanny.base_views import NannyFormView
from nanny.utilities import app_id_finder
from dbs_app.forms.dbs_details import CaptiaDBSDetailsForm


class CapitaDBSDetailsFormView(NannyFormView):
    template_name = 'capita-dbs-details.html'
    form_class = CaptiaDBSDetailsForm
    success_url = None

    def form_valid(self, form):
        application_id = self.request.GET['id']
        criminal_checks_record = NannyGatewayActions().read('dbs-check', params={'application_id': application_id}).record

        dbs_number = form.cleaned_data['dbs_number']
        has_convictions = form.cleaned_data['has_convictions']

        if has_convictions:
            self.success_url = 'dbs:Post-DBS-Certificate'
        elif not has_convictions:
            self.success_url = 'dbs:Criminal-Record-Check-Summary-View'
        else:
            raise ValueError('The field "has_convictions" is not equal to either True or False.')

        criminal_checks_record['dbs_number'] = dbs_number
        criminal_checks_record['has_convictions'] = has_convictions

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
        initial['has_convictions'] = dbs_record['has_convictions']
        return initial
