from nanny.base_views import NannyFormView
from nanny.db_gateways import NannyGatewayActions
from dbs_app.forms.dbs_type import DBSTypeForm


class DBSTypeFormView(NannyFormView):
    form_class = DBSTypeForm
    success_url = None
    template_name = 'dbs-type.html'

    def get_success_url(self):
        if self.request.POST['is_ofsted_dbs'] == 'True':
            self.success_url = 'dbs:Capita-DBS-Details-View'
        elif self.request.POST['is_ofsted_dbs'] == 'False':
            self.success_url = 'dbs:DBS-Update-Service-Page'
        else:
            raise ValueError('The field "is_ofsted_dbs" is not equal to one of "True" or "False".')

        return super(DBSTypeFormView, self).get_success_url()

    def form_valid(self, form):
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': self.request.GET['id']})

        criminal_checks_record = api_response.record
        criminal_checks_record['is_ofsted_dbs'] = self.request.POST['is_ofsted_dbs']

        NannyGatewayActions().put('dbs-check', params=criminal_checks_record)

        return super(DBSTypeFormView, self).form_valid(form)
