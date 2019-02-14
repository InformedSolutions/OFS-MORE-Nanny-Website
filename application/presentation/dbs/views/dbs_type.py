from application.presentation.base_views import NannyFormView
from application.services.db_gateways import NannyGatewayActions
from application.presentation.utilities import app_id_finder
from ..forms.dbs_type import DBSTypeForm


class DBSTypeFormView(NannyFormView):
    form_class = DBSTypeForm
    success_url = None
    template_name = 'dbs-type.html'

    def get_success_url(self):
        enhanced_check = self.criminal_checks_record['enhanced_check']
        on_update = self.request.POST['on_dbs_update_service']
        if not enhanced_check:
            self.success_url = 'dbs:DBS-Update-Service-Page'
        elif enhanced_check and (on_update == 'True'):
            self.success_url = 'dbs:DBS-Update-Service-Page'
        elif enhanced_check and (on_update == 'False'):
            self.success_url = 'dbs:DBS-Update-Service-Page'
        else:
            raise ValueError('The field "is_ofsted_dbs" is not equal to one of "True" or "False".')

        return super(DBSTypeFormView, self).get_success_url()

    def form_valid(self, form):
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': self.request.GET['id']})

        self.criminal_checks_record = api_response.record
        if self.criminal_checks_record['is_ofsted_dbs'] != True:
            self.criminal_checks_record['enhanced_check'] = self.request.POST['enhanced_check']
        self.criminal_checks_record['on_dbs_update_service'] = self.request.POST['on_dbs_update_service']

        NannyGatewayActions().put('dbs-check', params=self.criminal_checks_record)

        return super(DBSTypeFormView, self).form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        application_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': application_id})
        dbs_record = api_response.record
        initial['is_ofsted_dbs'] = dbs_record['is_ofsted_dbs']
        initial['enhanced_check'] = dbs_record['enhanced_check']
        initial['on_dbs_update_service'] = dbs_record['on_dbs_update_service']
        return initial


