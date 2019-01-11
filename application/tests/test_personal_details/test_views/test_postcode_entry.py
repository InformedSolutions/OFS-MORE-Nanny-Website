from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from application.presentation.personal_details.views import *
import uuid
from django.template.response import TemplateResponse

from application.tests.test_utils import side_effect
from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class PostcodeEntryTests(PersonalDetailsTests):

    def test_postcode_entry_url_resolves_to_page(self):
        """
        Test to assert that the 'postcode entry' page can be resolved.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
            mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
            mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

        found = resolve(reverse('personal-details:Personal-Details-Home-Address'))

        self.assertEqual(found.func.__name__, PersonalDetailHomeAddressView.__name__)

    def test_can_render_postcode_entry_page(self):
        """
        Test to assert that the 'postcode entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
            mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
            mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:

            nanny_api_read.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.uuid4()
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_update_address_valid_postcode_entry_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
            mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
            mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.UUID
            }), {
                'postcode': 'WA14 4PA'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/select-home-address/' in response.url)

    def test_can_create_address_valid_postcode_entry_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
            mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
            mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.UUID
            }), {
                'postcode': 'WA14 4PA'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/select-home-address/' in response.url)

    def test_can_submit_invalid_postcode_entry_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
            mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
            mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.UUID
            }), {
                'postcode': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


