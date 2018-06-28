from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class ManualEntryTests(PersonalDetailsTests):

    def test_manual_entry_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Manual-Address'))
        self.assertEqual(found.func.__name__, PersonalDetailManualAddressView.__name__)

    def test_can_render_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.get_record') as nanny_api_get_addr:
            nanny_api_get_addr.return_value.status_code = 200
            nanny_api_get_addr.return_value.record = self.sample_addr
            response = self.client.get(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_update_address_valid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """

        with mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.get_record') as nanny_api_get_addr, \
            mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.put') as nanny_api_put_addr:

            nanny_api_get_addr.return_value.status_code = 200
            nanny_api_get_addr.return_value.record = self.sample_addr

            nanny_api_put_addr.return_value.status_code = 200

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                'street_line1': 'Test',
                'street_line2': '',
                'town': 'test',
                'county': '',
                'postcode': 'WA14 4PA'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/home-address-details/' in response.url)

    def test_can_create_address_valid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """

        with mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.get_record') \
                as nanny_api_get_pd, \
            mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.get_record') as nanny_api_get_addr, \
            mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.create') as nanny_api_create_addr:
            nanny_api_get_pd.return_value.status_code = 200
            nanny_api_get_pd.return_value.record = self.sample_pd

            nanny_api_get_addr.return_value.status_code = 404

            nanny_api_create_addr.return_value.status_code = 201

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                'street_line1': 'Test',
                'street_line2': '',
                'town': 'test',
                'county': '',
                'postcode': 'WA14 4PA'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/home-address-details/' in response.url)

    def test_can_submit_invalid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """

        with mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.get_record') \
                as nanny_api_get_pd, \
            mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.get_record') as nanny_api_get_addr:
            nanny_api_get_pd.return_value.status_code = 200
            nanny_api_get_pd.return_value.record = self.sample_pd

            nanny_api_get_addr.return_value.status_code = 200
            nanny_api_get_addr.return_value.record = self.sample_addr

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                'street_line1': '',
                'street_line2': '',
                'town': '',
                'county': '',
                'postcode': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


