from ..test_base import *
from django.urls import resolve
from ...views.summary import *

class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id, *args, **kwargs):
    record = {
            'application_id': application_id,
            'email': 'test@informed.com'
        }
    return CustomResponse(record)


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class SummaryTests(InsuranceCoverTests):

    def test_summary_url_resolves_to_page(self):
        """
        Test to assert that the url for the 'summary' page can be resolved.
        """
        found = resolve(reverse('insurance:Summary'))
        self.assertEqual(found.func.__name__, SummaryView.__name__)

    def test_can_render_summary_page(self):
        """
        Test to assert that the summary page can be rendered
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            response = self.client.get(build_url('insurance:Summary', get={
                'id': self.application_id
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_post_to_summary_page(self):
        """
        Test to assert that the summary page can be rendered
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get_app, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put_app:

            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app
            response = self.client.post(build_url('insurance:Summary', get={
                'id': self.application_id
            }))

            self.assertEqual(response.status_code, 302)
            self.assertTrue('task-list' in response.url)
