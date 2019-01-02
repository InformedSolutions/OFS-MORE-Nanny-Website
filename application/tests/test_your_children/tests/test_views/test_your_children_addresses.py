from ..tests import authenticate, YourChildrenTests
from django.urls import resolve, reverse
from unittest import mock
from application.presentation.your_children.views import *
import uuid
from django.template.response import TemplateResponse

from application.tests.test_utils import side_effect

from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class Addresses(YourChildrenTests):

    def test_name_resolves_to_page(self):
        found = resolve(reverse('your-children:Your-Children-addresses'))
        self.assertCountEqual(found.func.__name__, YourChildrenAddressesView.__name__)

    def test_can_render_addresses_page(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('your-children:Your-Children-addresses', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_addresses_page(self):
        # with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
        #     nanny_api_read.side_effect = side_effect
        #     nanny_api_put.side_effect = side_effect
        #
        #     response = self.client.post(build_url('your-children:Your-Children-addresses', get={
        #         'id': uuid.uuid4()
        #     }), )
        #
        #     self.assertEqual(response.status_code, 200)
        #     self.assertTrue('your-children/address/' in response.url)
        self.skipTest('Not yet implemented')
