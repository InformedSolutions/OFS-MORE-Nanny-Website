from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class LivedAbroadTests(PersonalDetailsTests):

    def test_lived_abroad_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Lived-Abroad'))
        self.assertEqual(found.func.__name__, PersonalDetailLivedAbroadView.__name__)

    def test_can_render_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read:
            nanny_api_read.side_effect = side_effect
            response = self.client.get(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_true_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be submitted.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }), {
                'lived_abroad': True
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/good-conduct-certificates/' in response.url)

    def test_can_submit_false_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be submitted.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }), {
                'lived_abroad': False
            })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/check-answers/' in response.url)

    def test_can_submit_invalid_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be submitted.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read:
            nanny_api_read.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }), {
                'lived_abroad': ''
            })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)
