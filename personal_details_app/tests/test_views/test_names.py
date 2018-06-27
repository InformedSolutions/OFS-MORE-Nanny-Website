from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class NameTests(PersonalDetailsTests):

    def test_name_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Name'))
        self.assertEqual(found.func.__name__, PersonalDetailNameView.__name__)

    def test_can_render_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """

        with mock.patch('nanny_models.applicant_personal_details.ApplicantPersonalDetails.api.get_record') \
                as nanny_api_get_pd:
            nanny_api_get_pd.return_value.status_code = 200
            nanny_api_get_pd.return_value.record = self.sample_pd

            response = self.client.get(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
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

            response = self.client.post(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.UUID
            }), {
                'first_name': 'Test',
                'last_name': 'Test'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/your-date-of-birth/' in response.url)

    def test_can_submit_invalid_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
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

            response = self.client.post(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.UUID
            }), {
                'first_name': '',
                'last_name': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


