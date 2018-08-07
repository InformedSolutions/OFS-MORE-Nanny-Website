from http.cookies import SimpleCookie
from unittest import mock

from django.shortcuts import reverse
from django.test import modify_settings, TestCase

from tasks_app.views import ApplcationCancelledTemplateView, CancelApplicationTemplateView


@modify_settings(MIDDLEWARE={
        'remove': [
            'middleware.CustomAuthenticationHandler',
        ]
    })
class TestCancelApplication(TestCase):

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})

    # ---------- #
    # HTTP Tests #
    # ---------- #

    def test_can_render_cancel_application_page(self):
        """
        Test applicant can render the 'Cancel-Application' page.
        """
        response = self.client.get(reverse('Cancel-Application'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, CancelApplicationTemplateView.as_view().__name__)

    def test_can_cancel_application(self):
        """
        Test applicant can cancel their application and remove all information supplied by that point.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.delete') as nanny_api_delete, \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.delete') as identity_api_delete:

            nanny_api_delete.return_value.status_code = 200
            identity_api_delete.return_value.status_code = 200

            response = self.client.post(reverse('Cancel-Application'))

            self.assertTrue(nanny_api_delete.called)
            self.assertTrue(identity_api_delete.called)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.resolver_match.func.__name__, ApplcationCancelledTemplateView.as_view().__name__))
