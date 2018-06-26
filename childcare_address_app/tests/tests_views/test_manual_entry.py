from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from django.template.response import TemplateResponse
from unittest import mock
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class ManualEntryTests(ChildcareAddressTests):

    def test_manual_entry_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Manual-Entry'))
        self.assertEqual(found.func.__name__, ChildcareAddressManualView.__name__)

    def test_can_render_manual_page_with_address_id(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_multiple:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = self.sample_address
            nanny_api_get_multiple.return_value.status_code = 404

            response = self.client.get(build_url('Childcare-Address-Manual-Entry', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_initial_manual_page(self):
        """
        Test submission of a valid address for a new address.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.create') as nanny_api_create_address, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_addresses:
            nanny_api_create_address.return_value.status_code = 201
            nanny_api_create_address.return_value.record = {
                'childcare_address_id': uuid.UUID
            }
            nanny_api_get_addresses.return_value.status_code = 404

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
        childcare_address_id = uuid.UUID
        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.put'), \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get_address, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_addresses:

            nanny_api_get_address.return_value.status_code = 200
            nanny_api_get_address.return_value.record = {
                'street_line1': 'test',
                'street_line2': None,
                'town': 'test',
                'county': None,
                'postcode': 'WA14 4PA'
            }
            nanny_api_get_addresses.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Manual-Entry',
                                                  get={'id': uuid.UUID,
                                                       'childcare_address_id': childcare_address_id}),
                                        {'street_line1': 'test',
                                         'street_line2': '',
                                         'town': 'test',
                                         'county': '',
                                         'postcode': 'WA14 4PA'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/details/' in response.url)

    def test_can_submit_invalid_manual_page(self):
        """
        Test submission of an invalid address for a new address.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.create') as nanny_api_create_address, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_multiple:
            nanny_api_create_address.return_value.status_code = 201
            nanny_api_create_address.return_value.record = {
                'childcare_address_id': uuid.UUID
            }
            nanny_api_get_multiple.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Manual-Entry',
                                                  get={'id': uuid.UUID}),
                                        {'street_line1': '',
                                         'street_line2': '',
                                         'town': '',
                                         'county': '',
                                         'postcode': 'WA14 4PA'})

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)

    