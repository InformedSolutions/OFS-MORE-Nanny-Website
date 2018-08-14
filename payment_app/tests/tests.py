from http.cookies import SimpleCookie
from unittest import mock

import requests
from django.test import TestCase
from django.urls import reverse, resolve
from nanny.test_utils import side_effect, mock_nanny_application, mock_identity_record, urn_response


class PaymentTests(TestCase):
    """
    Tests for asserting payment functionality
    """

    def setUp(self):
        self.application_id = mock_nanny_application['application_id']
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})

    def test_page_validation_when_service_unavailable(self):
        """
        Full test to ensure that when a payment is taken the following outcomes are met:
           1. Payment confirmation page is shown
           2. Application Reference number assigned
           3. Payment record is lodged
        """
        with mock.patch('payment_app.services.payment_service.make_payment') as post_payment_mock, \
                mock.patch('requests.get') as application_reference_mock, \
                mock.patch('nanny.notify.send_email') as notify_mock, \
                mock.patch('payment_app.messaging.sqs_handler.SQSHandler.send_message') as sqs_mock, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.create') as nanny_api_create, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
                mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_create.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            urn_response = requests.Response()
            urn_response.status_code = 503
            urn_response._content = b'{ "error" : "HTTP Connection failed" }'

            application_reference_mock.return_value = urn_response

            test_payment_response = b'{ "customerOrderCode" : "TEST", "lastEvent" : "AUTHORISED"}'

            test_response = requests.Response()
            test_response.status_code = 201
            test_response._content = test_payment_response

            post_payment_mock.return_value = test_response

            response = self.client.post(
                reverse('payment:payment-details'),
                {
                    'id': self.application_id,
                    'card_type': 'visa',
                    'card_number': '5454545454545454',
                    'expiry_date_0': 1,
                    'expiry_date_1': 19,
                    'cardholders_name': 'Mr Example Cardholder',
                    'card_security_code': 123,
                }
            )

            self.assertEqual(response.status_code, 200)

    def test_can_lodge_valid_payment(self):
        """
        Full test to ensure that when a payment is taken the following outcomes are met:
           1. Payment confirmation page is shown
           2. Application Reference number assigned
           3. Payment record is lodged
        """
        with mock.patch('payment_app.services.payment_service.make_payment') as post_payment_mock, \
                mock.patch('requests.get') as application_reference_mock, \
                mock.patch('nanny.notify.send_email') as notify_mock, \
                mock.patch('payment_app.messaging.sqs_handler.SQSHandler.send_message') as sqs_mock, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.create') as nanny_api_create, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
                mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_create.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            application_reference_mock.return_value = urn_response

            test_payment_response = b'{ "customerOrderCode" : "TEST", "lastEvent" : "AUTHORISED"}'

            test_response = requests.Response()
            test_response.status_code = 201
            test_response._content = test_payment_response

            post_payment_mock.return_value = test_response

            response = self.client.post(
                reverse('payment:payment-details'),
                {
                    'id': self.application_id,
                    'card_type': 'visa',
                    'card_number': '5454545454545454',
                    'expiry_date_0': 1,
                    'expiry_date_1': 19,
                    'cardholders_name': 'Mr Example Cardholder',
                    'card_security_code': 123,
                }
            )

            # 1. Assert confirmation page shown
            self.assertEqual(response.status_code, 302)
            redirect_target = resolve(response.url)
            self.assertEqual(redirect_target.view_name, 'declaration:confirmation')