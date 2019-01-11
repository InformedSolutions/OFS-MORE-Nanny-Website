from application.presentation.base_views import NannyFormView
from application.services.db_gateways import NannyGatewayActions
from application.presentation.utilities import app_id_finder
from ..forms.dbs_update_service import DBSUpdateServiceForm


class DBSUpdateServiceFormView(NannyFormView):
    form_class = DBSUpdateServiceForm
    success_url = None
    template_name = 'dbs-update-service.html'

    def get_success_url(self):
        if self.request.POST['on_dbs_update_service'] == 'True':
            self.success_url = 'dbs:Non-Capita-DBS-Details-View'
        elif self.request.POST['on_dbs_update_service'] == 'False':
            self.success_url = 'dbs:Get-A-DBS-View'
        else:
            raise ValueError('The field "on_dbs_update_service" is not equal to one of "True" or "False"')

        return super(DBSUpdateServiceFormView, self).get_success_url()

    def form_valid(self, form):
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': self.request.GET['id']})

        criminal_checks_record = api_response.record
        criminal_checks_record['on_dbs_update_service'] = self.request.POST['on_dbs_update_service']

        NannyGatewayActions().put('dbs-check', params=criminal_checks_record)

        return super(DBSUpdateServiceFormView, self).form_valid(form)

    def get_initial(self):
        initial = super().get_initial()

        application_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
        dbs_record = api_response.record
        initial['on_dbs_update_service'] = dbs_record['on_dbs_update_service']
        return initial
