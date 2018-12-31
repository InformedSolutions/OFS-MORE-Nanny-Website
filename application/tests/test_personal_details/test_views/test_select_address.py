from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from application.presentation.personal_details.views import *
import uuid
from django.template.response import TemplateResponse

from application.tests.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class SelectAddressTests(PersonalDetailsTests):

    def test_select_address_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Select-Address'))
        self.assertEqual(found.func.__name__, PersonalDetailSelectAddressView.__name__)

    def test_can_render_select_address_page(self):
        """
        Test to assert that the 'select address' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read:
            nanny_api_read.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Select-Address', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_update_address_valid_select_address_page(self):
        """
        Test to assert that the 'select address' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Select-Address', get={
                'id': uuid.UUID
            }), {
                                            'address': 1
                                        })

            self.assertEqual(response.status_code, 200)

    def test_can_submit_invalid_select_address_page(self):
        """
        Test to assert that the 'select address' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Select-Address', get={
                'id': uuid.UUID
            }), {'postcode': ''})

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)
