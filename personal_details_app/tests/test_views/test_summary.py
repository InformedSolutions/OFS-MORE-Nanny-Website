from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve
from unittest import mock
from ...views import *
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class SummaryTests(PersonalDetailsTests):

    def test_summary_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Summary'))
        self.assertEqual(found.func.__name__, Summary.__name__)

    def test_can_render_summary_page(self):
        """
        Test to assert that the 'summary' page can be rendered.
        """
        with mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.get_record') \
                as nanny_api_get_pd, \
                mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.get_record') \
                as nanny_api_get_addr:
            nanny_api_get_pd.return_value.status_code = 200
            nanny_api_get_pd.return_value.record = self.sample_pd

            nanny_api_get_addr.return_value.status_code = 200
            nanny_api_get_addr.return_value.record = self.sample_addr

            response = self.client.get(build_url('personal-details:Personal-Details-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)
