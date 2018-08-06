from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve
from unittest import mock
from ...views import *
import uuid

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class SummaryTests(PersonalDetailsTests):

    def test_summary_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Summary'))
        self.assertEqual(found.func.__name__, Summary.__name__)

    def test_can_render_summary_page(self):
        """
        Test to assert that the 'summary' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)
