from ..tests import authenticate, YourChildrenTests
from django.urls import resolve, reverse
from unittest import mock
from application.presentation.your_children.views import *
import uuid
from django.template.response import TemplateResponse

from application.tests.test_utils import side_effect

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class DetailsTest(YourChildrenTests):

    def test_name_resolves_to_page(self):
        found = resolve(reverse('your-children:Your-Children-Details'))
        self.assertCountEqual(found.func.__name__, YourChildrenDetailsView.__name__)

    def test_can_render_name_page(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('your-children:Your-Children-Details', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_child_page(self):
        # with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
        #     nanny_api_read.side_effect = side_effect
        #     nanny_api_put.side_effect = side_effect
        #
        #     response = self.client.post(
        #         build_url('your-children:Your-Children-Details', get={'id': str(uuid.uuid4())}),
        #         data=
        #         {
        #             'id': uuid.uuid4(),
        #             'first_name': '',
        #             'last_name': '',
        #             'date_of_birth_0': '',
        #             'date_of_birth_1': '',
        #             'date_of_birth_2': '',
        #             'child': str(1),
        #             'children': str(1)
        #         }
        #     )
        #     self.assertEqual(response.status_code, 302)
        #     self.assertTrue('your-children/addresses/' in response.url)
        self.skipTest('Not yet implemented')

    def test_can_add_child(self):
        pass

    def test_can_remove_child(self):
        pass

    def test_can_submit_invalid_child_page(self):
        # with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
        #         mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
        #     nanny_api_read.side_effect = side_effect
        #     nanny_api_put.side_effect = side_effect
        #
        #     response = self.client.post(
        #         build_url('your-children:Your-Children-Details', get={'id': str(uuid.uuid4())}),
        #         data=
        #         {
        #             'id': uuid.uuid4(),
        #             'first_name': '',
        #             'last_name': '',
        #             'date_of_birth_0': '',
        #             'date_of_birth_1': '',
        #             'date_of_birth_2': '',
        #             'children': 1,
        #         }
        #     )
        #
        #     self.assertEqual(response.status_code, 200)
        #     self.assertTrue(type(response) == TemplateResponse)
        self.skipTest('Not yet implemented')
