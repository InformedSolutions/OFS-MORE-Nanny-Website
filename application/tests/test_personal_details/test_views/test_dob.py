from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from application.presentation.personal_details.views import *
import uuid
from django.template.response import TemplateResponse

from application.tests.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class DateOfBirthTests(PersonalDetailsTests):

    def test_dob_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Date-Of-Birth'))
        self.assertEqual(found.func.__name__, PersonalDetailDOBView.__name__)

    def test_can_render_dob_page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get_pd, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_get_pd.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_dob__page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """

        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get_pd, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_get_pd.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.uuid4()
            }), {
                'date_of_birth_0': '23',
                'date_of_birth_1': '08',
                'date_of_birth_2': '1997'
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/your-home-address/' in response.url)

    def test_can_submit_invalid_dob_page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.UUID
            }), {
                'date_of_birth_0': '',
                'date_of_birth_1': '',
                'date_of_birth_2': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


