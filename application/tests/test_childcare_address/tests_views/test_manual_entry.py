from ..tests import ChildcareAddressTests, authenticate
from application.presentation.childcare_address.views import *
from django.urls import resolve
from django.template.response import TemplateResponse
from unittest import mock
import uuid

from application.tests.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class ManualEntryTests(ChildcareAddressTests):

    def test_manual_entry_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Manual-Entry'))
        self.assertEqual(found.func.__name__, ChildcareAddressManualView.__name__)

    def test_can_render_manual_page_with_address_id(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.get(build_url('Childcare-Address-Manual-Entry', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_initial_manual_page(self):
        """
        Test submission of a valid address for a new address.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_create.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Manual-Entry',
                                                  get={'id': uuid.UUID}),
                                        {'street_line1': 'test',
                                         'street_line2': '',
                                         'town': 'test',
                                         'county': '',
                                         'postcode': 'WA14 4PA'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/details/' in response.url)

    def test_can_submit_existing_manual_page(self):
        """
        Test submission of a valid address for an existing address.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Manual-Entry',
                                                  get={'id': uuid.uuid4(),
                                                       'childcare_address_id': uuid.uuid4()}),
                                        {'street_line1': 'test',
                                         'street_line2': '',
                                         'town': 'test',
                                         'county': '',
                                         'postcode': 'WA14 4PA',
                                         'application_id': '998fd8ec-b96b-4a71-a1a1-a7a3ae186729',
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/details/' in response.url)

    def test_can_submit_invalid_manual_page(self):
        """
        Test submission of an invalid address for a new address.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Manual-Entry',
                                                  get={'id': uuid.UUID}),
                                        {'street_line1': '',
                                         'street_line2': '',
                                         'town': '',
                                         'county': '',
                                         'postcode': 'WA14 4PA'})

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)
