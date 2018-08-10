import json
import uuid
from unittest import mock

from django.test import TestCase
from django.urls import reverse, resolve
from nanny.db_gateways import NannyGatewayActions


class PaymentTests(TestCase):
    """
    Tests for asserting payment functionality
    """

    def setUp(self):
        pass

    def test_can_lodge_valid_payment(self):
        """
        Full test to ensure that when a payment is taken the following outcomes are met:
           1. Payment confirmation page is shown
           2. Application Reference number assigned
           3. Payment record is lodged
        """

        with mock.patch('application.services.payment_service.make_payment') as post_payment_mock, \
                mock.patch(
                    'application.services.noo_integration_service.create_application_reference') as application_reference_mock, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read:

            app_id = uuid.UUID()
            nanny_api_read.return_value = {
                'application_id': app_id
            }

            application_reference_mock.return_value = 'TESTURN'

            test_payment_response = {
                "customerOrderCode": "TEST",
                "lastEvent": "AUTHORISED"
            }

            post_payment_mock.return_value.status_code = 201
            post_payment_mock.return_value.text = json.dumps(test_payment_response)

            response = self.client.post(
                reverse('payment-details'),
                {
                    'id': app_id,
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
            self.assertEqual(redirect_target.view_name, 'Payment-Confirmation')

            # 2. Assert application reference assigned and marked as submitted
            application_record = NannyGatewayActions().read('application',
                                                            params={'application_id': application_id}).record
            self.assertIsNotNone(application.application_reference)
            self.assertIsNotNone(application.date_submitted)

            # 3.Assert payment record created and marked appropriately
            payment_record = Payment.objects.get(application_id=self.app_id)
            self.assertIsNotNone(payment_record.payment_reference)
            self.assertTrue(payment_record.payment_submitted)
            self.assertTrue(payment_record.payment_authorised)
