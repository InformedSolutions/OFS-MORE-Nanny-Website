from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class ManualEntryTests(PersonalDetailsTests):

    def test_manual_entry_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Manual-Address'))
        self.assertEqual(found.func.__name__, PersonalDetailManualAddressView.__name__)

    def test_can_render_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_update_address_valid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                'street_line1': 'Test',
                'street_line2': '',
                'town': 'test',
                'county': '',
                'postcode': 'WA14 4PA'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/home-address-details/' in response.url)

    def test_can_create_address_valid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                'street_line1': 'Test',
                'street_line2': '',
                'town': 'test',
                'county': '',
                'postcode': 'WA14 4PA'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/home-address-details/' in response.url)

    def test_can_submit_invalid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                'street_line1': '',
                'street_line2': '',
                'town': '',
                'county': '',
                'postcode': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


