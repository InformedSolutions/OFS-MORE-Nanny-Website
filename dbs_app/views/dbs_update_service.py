from nanny.base_views import NannyFormView
from nanny.db_gateways import NannyGatewayActions
from dbs_app.forms.dbs_update_service import DBSUpdateServiceForm


class DBSUpdateServiceFormView(NannyFormView):
    form_class = DBSUpdateServiceForm
    success_url = None
    template_name = 'dbs-update-service.html'

    def get_success_url(self):
        if self.request.POST['on_dbs_update_service']:
            self.success_url = 'dbs:Non-Capita-DBS-Details-View'
        else:
            self.success_url = 'dbs:Get-A-DBS-View'
        return super(DBSUpdateServiceFormView, self).get_success_url()

    def form_valid(self, form):
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': self.request.GET['id']})

        criminal_checks_record = api_response.record
        criminal_checks_record['on_dbs_update_service'] = self.request.POST['on_dbs_update_service']

        NannyGatewayActions().put('dbs-check', params=criminal_checks_record)

        return super(DBSUpdateServiceFormView, self).form_valid(form)
