from application.presentation.base_views import NannyTemplateView
from application.presentation.utilities import app_id_finder
from application.services.db_gateways import NannyGatewayActions


class DBSSignUpView(NannyTemplateView):
    """
    Template view to render the DBS sign-up page.
    """
    template_name = 'dbs-sign-up.html'
    success_url_name = 'Task-List'

    def get_context_data(self, **kwargs):
        context = super(NannyTemplateView, self).get_context_data(**kwargs)
        application_id = app_id_finder(self.request)

        # Set task status to 'Started'
        NannyGatewayActions().patch('application',
                                    params={'application_id': application_id, 'dbs_status': 'IN_PROGRESS'})

        return context
