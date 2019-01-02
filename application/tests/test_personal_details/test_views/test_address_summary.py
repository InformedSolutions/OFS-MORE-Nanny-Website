from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve
from unittest import mock
from application.presentation.personal_details.views import *
import uuid

from application.tests.test_utils import side_effect
from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions


@mock.patch.objecT(IdentityGatewayActions, "read", authenticate)
class AddressSummaryTests(PersonalDetailsTests):

    def test_address_summary_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Address-Summary'))
        self.assertEqual(found.func.__name__, PersonalDetailSummaryAddressView.__name__)

    def test_can_render_address_summary_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get_addr:
            nanny_api_get_addr.side_effect = side_effect
            response = self.client.get(build_url('personal-details:Personal-Details-Address-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_post_address_summary_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get_addr:
            nanny_api_get_addr.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Address-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/lived-abroad/' in response.url)
