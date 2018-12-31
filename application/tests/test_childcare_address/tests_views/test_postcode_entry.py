from ..tests import ChildcareAddressTests, authenticate
from application.presentation.childcare_address.views import *
from django.urls import resolve
from django.template.response import TemplateResponse
from unittest import mock
import uuid

from application.tests.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class PostcodeEntryTests(ChildcareAddressTests):

    def test_postcode_entry_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Postcode-Entry'))
        self.assertEqual(found.func.__name__, ChildcareAddressPostcodeView.__name__)

    def test_can_render_postcode_entry_page(self):
        """
        Test to assert that the 'postcode entry' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.get(build_url('Childcare-Address-Postcode-Entry', get={'id': uuid.UUID}))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_initial_postcode_entry_page(self):
        """
        Test submission of a valid postcode for a new address.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.create') as nanny_api_create:

            nanny_api_create.return_value.status_code = 201
            nanny_api_create.return_value.record = {
                'childcare_address_id': uuid.UUID
            }

            response = self.client.post(build_url('Childcare-Address-Postcode-Entry', get={'id': uuid.UUID}),
                                        {'postcode': 'WA14 4PA'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue('select-childcare-address' in response.url)

    def test_can_submit_valid_existing_postcode_entry_page(self):
        """
        Test submission of a valid postcode for a new address.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Postcode-Entry',
                                                  get={'id': uuid.UUID,'childcare_address_id': uuid.UUID}),
                                        {'postcode': 'WA14 4PA'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue('select-childcare-address' in response.url)

    def test_can_submit_invalid_postcode_entry_page(self):
        """
        Test submission of a valid postcode for a new address.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Postcode-Entry',
                                                  get={'id': uuid.UUID}),
                                        {'postcode': None})

            self.assertEqual(response.status_code, 200)
            # check if we get a template back (synonymous with an invalid form submission)
            self.assertTrue(type(response) == TemplateResponse)
