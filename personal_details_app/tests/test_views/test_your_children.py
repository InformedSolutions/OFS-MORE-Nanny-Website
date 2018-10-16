from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class YourChildrenTests(PersonalDetailsTests):

    def test_your_children_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Your-Children'))
        self.assertEqual(found.func.__name__, PersonalDetailsYourChildrenView.__name__)

    def test_can_render_your_children_page(self):
        """
        Test to assert that the 'your children' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            response = self.client.get(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_true_your_children_page(self):
        """
        Test to assert that the 'your children' page can be submitted.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
               mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
               mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch, \
               mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }), {
                'your_children': True
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/check-answers/' in response.url)

    def test_can_submit_your_children_page(self):
        """
        Test to assert that the 'your children' page can be submitted.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }), {
                'your_children': False
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/check-answers/' in response.url)

    def test_can_submit_invalid_your_children_page(self):
        """
        Test to assert that the 'your children' page can be submitted.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }), {
                'lived_abroad': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)