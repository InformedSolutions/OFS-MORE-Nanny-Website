from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from unittest import mock
import uuid

from nanny.test_utils import side_effect, mock_childcare_address_record


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class ManualEntryTests(ChildcareAddressTests):
    def test_address_details_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Details'))
        self.assertEqual(found.func.__name__, ChildcareAddressDetailsView.__name__)

    def test_can_render_address_details_page(self):
        """
        Test to assert that the 'address details' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            # nanny_api_get_multiple.return_value.record = [self.sample_address]

            response = self.client.get(build_url('Childcare-Address-Details', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_redirected_when_adding_another(self):
        """
        Test to assert that another address can be added.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

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
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            # Assert list call returns five records.
            nanny_api_list.return_value.record = [mock_childcare_address_record, mock_childcare_address_record,
                                                  mock_childcare_address_record, mock_childcare_address_record,
                                                  mock_childcare_address_record]
            nanny_api_list.return_value.status_code = 200

            response = self.client.post(build_url('Childcare-Address-Details', get={
                'id': uuid.UUID
            }), {
                'add_another': ''
            })

            # test that we have not been re-directed
            self.assertEqual(response.status_code, 200)

    def test_redirected_when_removing_last_address(self):
        """
        Test to assert that the applicant is redirected to the Where you work page if they have removed the last address
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list,\
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            # Assert list call returns five records.
            nanny_api_list.return_value.record = [mock_childcare_address_record]
            nanny_api_list.return_value.status_code = 200

            response = self.client.get(build_url('Childcare-Address-Details', get={
                'id': mock_childcare_address_record['application_id'],
                'childcare-address-id': mock_childcare_address_record['childcare_address_id']
            }))

            print(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertTrue('where-you-work' in response.url)
