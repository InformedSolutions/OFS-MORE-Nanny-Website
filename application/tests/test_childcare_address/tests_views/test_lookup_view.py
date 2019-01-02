from ..tests import ChildcareAddressTests, authenticate
from application.presentation.childcare_address.views import *
from django.urls import resolve
from unittest import mock
from django.template.response import TemplateResponse
import uuid

from application.tests.test_utils import side_effect

from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class LookupViewTests(ChildcareAddressTests):

    def test_select_address_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Lookup'))
        self.assertEqual(found.func.__name__, ChildcareAddressLookupView.__name__)

    def test_can_render_lookup_page(self):
        """
        Test to assert that the 'address lookup' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.get(build_url('Childcare-Address-Lookup', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_lookup_page(self):
        """
        Test to assert that the 'address lookup' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

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
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404

            response = self.client.post(build_url('Childcare-Address-Lookup', get={
                'id': uuid.UUID,
                'childcare_address_id': uuid.UUID
            }), {'address': ''})

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)

