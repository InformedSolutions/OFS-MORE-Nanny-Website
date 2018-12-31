from ..tests import authenticate, YourChildrenTests
from django.urls import resolve, reverse
from unittest import mock
from application.presentation.your_children.views import *
import uuid

from application.tests.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class PostcodeTest(YourChildrenTests):

    def test_name_resolves_to_page(self):
        found = resolve(reverse('your-children:Your-Children-Postcode'))
        self.assertCountEqual(found.func.__name__, YourChildrenPostcodeView.__name__)

    def test_can_render_postcode_page(self):
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            response = self.client.get(
                build_url('your-children:Your-Children-Postcode', get={'id': str(uuid.uuid4())}),
                data=
                {
                    'id': uuid.uuid4(),
                    'child': str(1),
                }
            )
            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_postcode_page(self):
        # with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
        #     nanny_api_read.side_effect = side_effect
        #     nanny_api_put.side_effect = side_effect
        #
        #     response = self.client.post(
        #         build_url('your-children:Your-Children-Postcode', get={'id': str(uuid.uuid4())}),
        #         data=
        #         {
        #             'postcode': 'WA14 2EY',
        #             'id': uuid.uuid4(),
        #             'child': str(1),
        #         }
        #     )
        #     self.assertEqual(response.status_code, 302)
        #     self.assertTrue('your-children-details/' in response.url)
        self.skipTest('Not yet implemented')

    def test_can_submit_invalid_postcode_page(self):
        self.skipTest('Not yet implemented')


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class AddressSelectTest(YourChildrenTests):

    def test_name_resolves_to_page(self):
        found = resolve(reverse('your-children:Your-Children-Address-Selection'))
        self.assertCountEqual(found.func.__name__, YourChildrenAddressSelectionView.__name__)

    def test_can_render_address_select_page(self):
        # with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
        #     nanny_api_read.side_effect = side_effect
        #     nanny_api_put.side_effect = side_effect
        #     response = self.client.get(
        #         build_url('your-children:Your-Children-Address-Selection', get={'id': str(uuid.uuid4())}),
        #         data=
        #         {
        #             'id': uuid.uuid4(),
        #             'child': str(1),
        #         }
        #     )
        #     self.assertEqual(response.status_code, 200)
        self.skipTest('Not yet implemented')


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class ManualAddressTest(YourChildrenTests):

    def test_name_resolves_to_page(self):
        found = resolve(reverse('your-children:Your-Children-Manual-address'))
        self.assertCountEqual(found.func.__name__, YourChildrenManualAddressView.__name__)

    def test_can_render_manual_address_page(self):
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            response = self.client.get(
                build_url('your-children:Your-Children-Manual-address', get={'id': str(uuid.uuid4())}),
                data=
                {
                    'id': uuid.uuid4(),
                    'child': str(1),
                }
            )
            self.assertEqual(response.status_code, 200)