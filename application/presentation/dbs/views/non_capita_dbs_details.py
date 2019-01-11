from application.services.db_gateways import NannyGatewayActions
from application.presentation.base_views import NannyFormView
from application.presentation.utilities import app_id_finder
from ..forms.dbs_details import NonCapitaDBSDetailsForm


class NonCapitaDBSDetailsFormView(NannyFormView):
    template_name = 'non-capita-dbs-details.html'
    form_class = NonCapitaDBSDetailsForm
    success_url = 'dbs:Post-DBS-Certificate'

    def form_valid(self, form):
        application_id = self.request.GET['id']

        criminal_checks_record = NannyGatewayActions().read('dbs-check', params={'application_id': application_id}).record
        criminal_checks_record['dbs_number'] = form.cleaned_data['dbs_number']

        NannyGatewayActions().put('dbs-check', params=criminal_checks_record)

        return super(NonCapitaDBSDetailsFormView, self).form_valid(form)

    def get_initial(self):
        initial = super().get_initial()

        application_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
        dbs_record = api_response.record
        initial['dbs_number'] = dbs_record['dbs_number']
        return initial
