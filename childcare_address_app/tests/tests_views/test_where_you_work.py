from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from django.template.response import TemplateResponse
from unittest import mock
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
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

        with mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = {
                'address_to_be_provided': True
            }

            response = self.client.get(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}))

            self.assertEqual(response.status_code, 200)

    # POST REQUEST TESTS (multiple scenarios) #

    def test_can_submit_valid_where_you_work_page_with_no_previous_addresses_true_resp(self):
        """
        Test that you are directed to the right page with a valid form and no previous addresses
        if you know where you are working.
        """

        with mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_put_app, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_addresses:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = {
                'address_to_be_provided': None
            }

            nanny_api_get_addresses.return_value.record = []

            response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                        {'address_to_be_provided': 'True'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue("childcare-location" in response.url)

    def test_can_submit_valid_where_you_work_page_with_no_previous_addresses_false_resp(self):
        """
        Test that you are directed to the right page with a valid form and no previous addresses
        if you do not know where you are working.
        """

        with mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_put_app, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_addresses:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = {
                'address_to_be_provided': None
            }

            nanny_api_get_addresses.return_value.record = []

            response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                        {'address_to_be_provided': 'False'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue("details-later" in response.url)

    def test_can_submit_valid_where_you_work_page_with_previous_addresses(self):
        """
        Test that you are directed to the right page with a valid form but have previous addresses
        """

        with mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_put_app, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_addresses:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = {
                'address_to_be_provided': None
            }

            nanny_api_get_addresses.return_value.record = [self.sample_address]
            nanny_api_get_addresses.return_value.status_code = 200

            response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                        {'address_to_be_provided': 'True'})

            self.assertEqual(response.status_code, 302)
            self.assertTrue("/details/" in response.url)

    def test_can_submit_invalid_where_you_work_page(self):
        """
        Test that you are directed to the right page with a valid form but have previous addresses
        """
        response = self.client.post(build_url('Childcare-Address-Where-You-Work', get={'id': uuid.UUID}),
                                    {'address_to_be_provided': None})

        self.assertEqual(response.status_code, 200)
        # check if we get a template back (synonymous with an invalid form submission)
        self.assertTrue(type(response) == TemplateResponse)
