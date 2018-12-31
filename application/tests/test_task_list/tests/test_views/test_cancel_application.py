from http.cookies import SimpleCookie
from unittest import mock
import uuid

from django.test import modify_settings, TestCase
from django.urls import resolve, reverse

from nanny.middleware import CustomAuthenticationHandler

from application.presentation.task_list.views import ApplicationCancelledTemplateView, CancelApplicationTemplateView


@modify_settings(MIDDLEWARE={
        'remove': [
            'nanny.middleware.CustomAuthenticationHandler',
        ]
    })
class TestCancelApplication(TestCase):

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
        self.example_uuid = str(uuid.uuid4())

    # ---------- #
    # HTTP Tests #
    # ---------- #

    def test_can_render_cancel_application_page(self):
        """
        Test applicant can render the 'Cancel-Application' page.
        """
        response = self.client.get(reverse('Cancel-Application') + '?id=' + self.example_uuid)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, CancelApplicationTemplateView.as_view().__name__)

    def test_can_cancel_application(self):
        """
        Test applicant can cancel their application and remove all information supplied by that point.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.delete') as nanny_api_delete, \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.delete') as identity_api_delete:

            nanny_api_delete.return_value.status_code = 204
            identity_api_delete.return_value.status_code = 204

            response = self.client.post(reverse('Cancel-Application') + '?id=' + self.example_uuid)

            self.assertTrue(nanny_api_delete.called)
            self.assertTrue(identity_api_delete.called)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(resolve(response.url).func.view_class, ApplicationCancelledTemplateView)

    def test_session_destroyed_upon_application_cancellation(self):
        """
        Test applicant has their session cookies destroyed upon cancelling their application.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.delete'), \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.delete'):

            response = self.client.post(reverse('Cancel-Application') + '?id=' + self.example_uuid)
            cookie_key = CustomAuthenticationHandler.get_cookie_identifier()

            self.assertEqual(response.cookies[cookie_key].value, '')
