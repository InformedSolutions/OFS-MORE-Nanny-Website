from nanny.base_views import NannyFormView
from nanny.db_gateways import NannyGatewayActions
from dbs_app.forms.lived_abroad import LivedAbroadForm


class LivedAbroadFormView(NannyFormView):
    form_class = LivedAbroadForm
    success_url = None
    template_name = 'lived-abroad.html'

    def get_success_url(self):
        if self.request.POST['lived_abroad'] == 'True':
            self.success_url = 'dbs:Criminal-Records-Abroad-View'
        elif self.request.POST['lived_abroad'] == 'False':
            self.success_url = 'dbs:DBS-Guidance-View'
        else:
            raise ValueError('The field "lived_abroad" is not equal to one of "True" or "False".')

        return super(LivedAbroadFormView, self).get_success_url()

    def form_valid(self, form):
        api_response = NannyGatewayActions().read('dbs-check', params={'application_id': self.request.GET['id']})

        if api_response.status_code == 404:  # If the Criminal record checks record is yet to be created.
            api_response = NannyGatewayActions().create('dbs-check', params={'application_id': self.request.GET['id']})

        criminal_checks_record = api_response.record
        criminal_checks_record['lived_abroad'] = self.request.POST['lived_abroad']

        NannyGatewayActions().put('dbs-check', params=criminal_checks_record)

        return super(LivedAbroadFormView, self).form_valid(form)
