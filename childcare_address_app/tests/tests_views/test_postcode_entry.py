from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from django.template.response import TemplateResponse
from unittest import mock
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class PostcodeEntryTests(ChildcareAddressTests):

    def test_postcode_entry_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Postcode-Entry'))
        self.assertEqual(found.func.__name__, ChildcareAddressPostcodeView.__name__)

    def test_can_render_postcode_entry_page(self):
        """
        Test to assert that the 'postcode entry' page can be rendered.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_multiple:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = {
                'postcode': 'WA14 4PA'
            }

            nanny_api_get_multiple.status_code = 404

            response = self.client.get(build_url('Childcare-Address-Postcode-Entry', get={'id': uuid.UUID}))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_initial_postcode_entry_page(self):
        """
        Test submission of a valid postcode for a new address.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.create') as nanny_api_create_address:
            nanny_api_create_address.return_value.status_code = 201
            nanny_api_create_address.return_value.record = {
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

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.put') as nanny_api_put_address, \
        mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get_address:
            nanny_api_get_address.return_value.status_code = 200
            nanny_api_get_address.return_value.record = {
                'postcode': "WA15 4PA"
            }

            nanny_api_put_address.return_value.status_code = 200

            response = self.client.post(build_url('Childcare-Address-Postcode-Entry',
                                                  get={'id': uuid.UUID,'childcare_address_id': uuid.UUID}),
                                        {'postcode': 'WA14 4PA'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue('select-childcare-address' in response.url)

    def test_can_submit_invalid_postcode_entry_page(self):
        """
        Test submission of a valid postcode for a new address.
        """
        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_multiple:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = {
                'postcode': 'WA14 4PA'
            }

            nanny_api_get_multiple.status_code = 404
            response = self.client.post(build_url('Childcare-Address-Postcode-Entry',
                                                  get={'id': uuid.UUID}),
                                        {'postcode': None})

            self.assertEqual(response.status_code, 200)
            # check if we get a template back (synonymous with an invalid form submission)
            self.assertTrue(type(response) == TemplateResponse)
