from nanny.base_views import NannyFormView
from nanny.utilities import app_id_finder
from ..forms.declaration import DeclarationForm

from nanny.db_gateways import NannyGatewayActions


class FinalDeclaration(NannyFormView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "final-declaration.html"
    success_url = 'payment:payment-details'
    form_class = DeclarationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['fields'] = [context['form'].render_field(name, field) for name, field in context['form'].fields.items()]
        return context

    def get_initial(self):
        initial = super().get_initial()
        app_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if api_response.status_code == 200:
            record = api_response.record
            initial['follow_rules'] = record['follow_rules']
            initial['share_info_declare'] = record['share_info_declare']
            initial['information_correct_declare'] = record['information_correct_declare']
            initial['change_declare'] = record['change_declare']
        return initial
