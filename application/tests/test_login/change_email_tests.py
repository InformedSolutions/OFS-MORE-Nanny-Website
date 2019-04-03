from unittest.mock import patch

from django.http import HttpResponse

from django.test import TestCase, tag, Client
from django.urls import reverse

from application.tests.test_utils import mock_nanny_application, mock_personal_details_record, mock_identity_record

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions

from django.test import modify_settings

@modify_settings(MIDDLEWARE={
        'remove': [
            'nanny.middleware.CustomAuthenticationHandler',
        ]
    })
class ChangeEmailTests(TestCase):

    def setUp(self):
        self.client = Client()
        base_url = reverse('Change-Email')
        self.base_url = base_url
        self.url = base_url + '?id=' + mock_nanny_application['application_id']

    # Unit Tests

    @tag('unit')
    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code == 200)

    @tag('unit')
    def test_post_request(self):
        response = self.client.post(self.url)
        self.assertTrue(response.status_code == 200)
        
    # Http Tests
        
    @tag('http')
    @patch('login_app.views.change_email.ChangeEmailTemplateView.form_valid')
    def test_form_valid_request(self, form_valid):
        mock_response = HttpResponse()
        mock_response.status_code = 200
        form_valid.return_value = mock_response
        form_valid.side_effect = None

        mock_data = {'change_email': 'test_email@informed.com'}

        response = self.client.post(reverse('Change-Email'), mock_data)

        form_valid.assert_called_once()
        
        
    @tag('http')
    def test_change_email_email_sent(self):
        client = self.client

        mock_personal_details_response = HttpResponse()
        mock_personal_details_response.record = mock_personal_details_record

        testing_change_email_email_sent(client, mock_personal_details_response)

    @tag('http')
    def test_change_email_email_sent_no_personal_details(self):
        client = self.client

        mock_personal_details_response = HttpResponse()
        mock_personal_details_response.record = None

        testing_change_email_email_sent(client, mock_personal_details_response)


@patch('login_app.views.change_email.ChangeEmailTemplateView.send_change_email_email')
@patch('login_app.views.change_email.NannyGatewayActions.read')
@patch.object(IdentityGatewayActions, 'read')
@patch.object(IdentityGatewayActions, 'put')
@patch('login_app.views.change_email.utilities.generate_email_validation_link')
def testing_change_email_email_sent(client, mock_personal_details_response,
                                    gen_magic_link=None,
                                    identity_put=None,
                                    identity_read=None,
                                    nanny_read=None,
                                    send_change_email=None):
    identity_read_mock_response = HttpResponse()
    identity_read_mock_response.record = mock_identity_record
    identity_read.return_value = identity_read_mock_response

    nanny_read.return_value = mock_personal_details_response


    gen_magic_link.return_value = ('http://localhost:8000/nanny/validate/IDXN1DSCZNSR', 1534774007)

    mock_data = {'change_email': 'test_email@informed.com'}

    # Send post request
    response = client.post(reverse('Change-Email'), mock_data)

    # 1. Assert a magic link was generated.
    gen_magic_link.assert_called_once()

    # 2. Assert the identity record was updated.
    identity_put.assert_called_once()

    # 3. Assert an email was sent.
    send_change_email.assert_called_once()
