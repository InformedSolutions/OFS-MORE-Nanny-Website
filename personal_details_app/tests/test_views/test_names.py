from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve, reverse
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class NameTests(PersonalDetailsTests):

    def test_name_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Name'))
        self.assertEqual(found.func.__name__, PersonalDetailNameView.__name__)

    def test_can_render_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.uuid4()
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
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.UUID
            }), {
                'first_name': '',
                'last_name': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)
