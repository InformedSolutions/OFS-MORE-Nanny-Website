import uuid
from unittest import mock

from django.template.response import TemplateResponse
from django.urls import resolve

from application.tests.test_utils import side_effect
from ..tests import ChildcareAddressTests, authenticate
from application.presentation.childcare_address.views import *

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class WhereYouWorkTests(ChildcareAddressTests):

    def test_where_you_work_url_resolves_to_page(self):
        """
        Test that the URL for the 'where you work' page resolves.
        """
        found = resolve(reverse('Childcare-Address-Where-You-Work'))
        self.assertEqual(found.func.__name__, WhereYouWorkView.__name__)

    def test_can_render_where_you_work_page(self):
        """
        Test to assert that the 'where you work' page can be rendered.
        """
        self.skipTest('FIXME')
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}))

            self.assertEqual(response.status_code, 200)

    # POST REQUEST TESTS (multiple scenarios) #

    def test_can_submit_valid_where_you_work_page_with_no_previous_addresses_true_resp(self):
        """
        Test that you are directed to the right page with a valid form and no previous addresses
        if you know where you are working.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404
            nanny_api_list.return_value.record = []

            response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                        {'address_to_be_provided': 'True'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue("childcare-location" in response.url)

    def test_can_submit_valid_where_you_work_page_with_no_previous_addresses_false_resp(self):
        """
        Test that you are directed to the right page with a valid form and no previous addresses
        if you do not know where you are working.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 404
            nanny_api_list.return_value.record = []

            response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                        {'address_to_be_provided': 'False'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue("details-later" in response.url)

    def test_can_submit_valid_where_you_work_page_with_previous_addresses(self):
        """
        Test that you are directed to the right page with a valid form but have previous addresses
        """
        self.skipTest('FIXME')
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            nanny_api_list.return_value.status_code = 200
            nanny_api_list.return_value.record = [self.sample_address]

            response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                        {'address_to_be_provided': 'True'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue("/childcare-location/" in response.url)

    def test_can_submit_invalid_where_you_work_page(self):
        """
        Test that you are directed to the right page with a valid form but have previous addresses
        """
        self.skipTest('FIXME')
        response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                    {'address_to_be_provided': None})

        self.assertEqual(response.status_code, 200)
        # check if we get a template back (synonymous with an invalid form submission)
        self.assertTrue(type(response) == TemplateResponse)
