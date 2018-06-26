from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from unittest import mock
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class ManualEntryTests(ChildcareAddressTests):
    def test_address_details_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Details'))
        self.assertEqual(found.func.__name__, ChildcareAddressDetailsView.__name__)

    def test_can_render_address_details_page(self):
        """
        Test to assert that the 'address details' page can be rendered.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_multiple:
            nanny_api_get_multiple.return_value.status_code = 200
            nanny_api_get_multiple.return_value.record = [self.sample_address]

            response = self.client.get(build_url('Childcare-Address-Details', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_redirected_when_adding_another(self):
        """
        Test to assert that another address can be added.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_multiple:
            nanny_api_get_multiple.return_value.status_code = 200
            nanny_api_get_multiple.return_value.record = [self.sample_address]
            response = self.client.post(build_url('Childcare-Address-Details', get={
                'id': uuid.UUID
            }), {
                'add_another': ''
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('childcare-address-postcode' in response.url)

    def test_cannot_add_more_than_five_addresses(self):
        """
        Test to assert that another address cannot be added if you already have five.
        """

        with mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_multiple:
            nanny_api_get_multiple.return_value.status_code = 200
            nanny_api_get_multiple.return_value.record = [self.sample_address, self.sample_address,
                                                          self.sample_address, self.sample_address,
                                                          self.sample_address]
            response = self.client.post(build_url('Childcare-Address-Details', get={
                'id': uuid.UUID
            }), {
                'add_another': ''
            })

            # test that we have not been re-directed
            self.assertEqual(response.status_code, 200)
