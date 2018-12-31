from ..base_tests import PersonalDetailsTests, authenticate
from django.urls import resolve
from unittest import mock
from application.presentation.personal_details.views import *
import uuid


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class CertificateTests(PersonalDetailsTests):

    def test_conduct_certificates_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Certificates-Of-Good-Conduct'))
        self.assertEqual(found.func.__name__, PersonalDetailCertificateView.__name__)

    def test_can_render_conduct_certificates_page(self):
        """
        Test to assert that the 'good conduct certificates' page can be rendered.
        """
        response = self.client.get(build_url('personal-details:Personal-Details-Certificates-Of-Good-Conduct', get={
            'id': uuid.UUID
        }))

        self.assertEqual(response.status_code, 200)

    def test_post_certificates_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Post-Certificates'))
        self.assertEqual(found.func.__name__, PersonalDetailsPostCertificateView.__name__)

    def test_can_render_post_certificates_page(self):
        """
        Test to assert that the 'good conduct certificates' page can be rendered.
        """
        response = self.client.get(build_url('personal-details:Personal-Details-Post-Certificates', get={
            'id': uuid.UUID
        }))

        self.assertEqual(response.status_code, 200)
