from ..test_base import *
from django.urls import resolve
from ...views.public_liability import *
from django.template.response import TemplateResponse


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
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
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get:
            nanny_api_get.return_value.status_code = 404
            response = self.client.get(build_url('insurance:Public-Liability', get={
                'id': self.application_id
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_false_public_liability_form(self):
        """
        Test to assert that user gets redirected to the insurance cover page
        if they do not have public liability insurance.
        """
        # FIXME
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get_app, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put_app:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app
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
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get_app, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put_app:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app
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
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_get:
            nanny_api_get.return_value.status_code = 200
            response = self.client.post(build_url('insurance:Public-Liability', get={
                'id': self.application_id
            }), {
                'public_liability': ''
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)
