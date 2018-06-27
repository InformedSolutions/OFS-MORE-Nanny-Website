from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class DateOfBirthTests(PersonalDetailsTests):

    def test_dob_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Date-Of-Birth'))
        self.assertEqual(found.func.__name__, PersonalDetailDOBView.__name__)

    def test_can_render_dob_page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """

        with mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.get_record') \
                as nanny_api_get_pd:
            nanny_api_get_pd.return_value.status_code = 200
            nanny_api_get_pd.return_value.record = self.sample_pd

            response = self.client.get(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_name_page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """

        with mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.get_record') \
                as nanny_api_get_pd, \
            mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.put') \
                as nanny_api_put_pd, \
            mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get_app, \
            mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_put_app:
            nanny_api_get_pd.return_value.status_code = 200
            nanny_api_get_pd.return_value.record = self.sample_pd

            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app

            nanny_api_put_app.return_value.status_code = 200
            nanny_api_get_pd.return_value.status_code = 200

            response = self.client.post(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.UUID
            }), {
                'date_of_birth': '2018-01-01'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/your-home-address/' in response.url)

    def test_can_submit_invalid_name_page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """

        with mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.get_record') \
                as nanny_api_get_pd, \
            mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.put') \
                as nanny_api_put_pd, \
            mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get_app, \
            mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_put_app:
            nanny_api_get_pd.return_value.status_code = 200
            nanny_api_get_pd.return_value.record = self.sample_pd

            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app

            nanny_api_put_app.return_value.status_code = 200
            nanny_api_get_pd.return_value.status_code = 200

            response = self.client.post(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.UUID
            }), {
                'day': '',
                'month': '',
                'year': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


