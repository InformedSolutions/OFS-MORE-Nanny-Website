from ..test_base import *
from django.urls import resolve
from application.presentation.insurance_cover.views.public_liability import *
from django.template.response import TemplateResponse

from application.tests.test_utils import side_effect

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id, *args, **kwargs):
    record = {
            'application_id': application_id,
            'email': 'test@informed.com'
        }
    return CustomResponse(record)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class PublicLiabilityTests(InsuranceCoverTests):

    def test_public_liability_url_resolves_to_page(self):
        """
        Test to assert that the url for the 'public liability' page can be resolved.
        """
        found = resolve(reverse('insurance:Public-Liability'))
        self.assertEqual(found.func.__name__, PublicLiabilityView.__name__)

    def test_can_render_public_liability_page(self):
        """
        Test to assert that the public liability page can be rendered
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('insurance:Public-Liability', get={
                'id': self.application_id
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_false_public_liability_form(self):
        """
        Test to assert that user gets redirected to the insurance cover page
        if they do not have public liability insurance.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('insurance:Public-Liability', get={
                'id': self.application_id
            }), {
                'public_liability': 'False'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('/get-insurance' in response.url)

    def test_can_submit_true_public_liability_form(self):
        """
        Test to assert that user gets redirected to the insurance cover page
        if they do not have public liability insurance.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('insurance:Public-Liability', get={
                'id': self.application_id
            }), {
                'public_liability': 'True'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue('/check-answers' in response.url)


    def test_can_submit_invalid_public_liability_form(self):
        """
        Test to assert that user gets redirected to the insurance cover page
        if they do not have public liability insurance.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
            mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_get.return_value.status_code = 200
            response = self.client.post(build_url('insurance:Public-Liability', get={
                'id': self.application_id
            }), {
                'public_liability': ''
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)
