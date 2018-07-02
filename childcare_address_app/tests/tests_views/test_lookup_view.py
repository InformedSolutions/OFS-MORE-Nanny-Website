from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from unittest import mock
from django.template.response import TemplateResponse
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class LookupViewTests(ChildcareAddressTests):

    def test_select_address_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Lookup'))
        self.assertEqual(found.func.__name__, ChildcareAddressLookupView.__name__)

    def test_can_render_lookup_page(self):
        """
        Test to assert that the 'address lookup' page can be rendered.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get_one, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_many:
            nanny_api_get_one.return_value.status_code = 200
            nanny_api_get_one.return_value.record = {
                'postcode': 'WA14 4PA'
            }
            nanny_api_get_many.return_value.status_code = 404

            response = self.client.get(build_url('Childcare-Address-Lookup', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_lookup_page(self):
        """
        Test to assert that the 'address lookup' page can be rendered.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get_address, \
        mock.patch('nanny_models.childcare_address.ChildcareAddress.api.put') as nanny_api_put, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_many:
            nanny_api_get_address.return_value.status_code = 200
            nanny_api_get_address.return_value.record = {
                'postcode': 'WA14 4PA'
            }

            nanny_api_get_many.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Lookup', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }), {'address': '1'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/details/' in response.url)

    def test_can_submit_invalid_lookup_page(self):
        """
        Test to assert that the 'address lookup' page can be rendered.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_record') as nanny_api_get_address, \
            mock.patch('nanny_models.childcare_address.ChildcareAddress.api.put') as nanny_api_put, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_many:
            nanny_api_get_address.return_value.status_code = 200
            nanny_api_get_address.return_value.record = {
                'postcode': 'WA14 4PA'
            }
            nanny_api_get_many.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Lookup', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }), {'address': ''})

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)

