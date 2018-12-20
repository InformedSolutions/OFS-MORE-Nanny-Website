import os
import time
from unittest import mock

from django.test import TestCase

from payment_app.services.payment_service import create_formatted_payment_reference


class PaymentTests(TestCase):
    """
    Tests for asserting payment functionality
    """
    def setUp(self):
        pass

    # def test_payment_reference_formatted(self):
    #     test_cm_reference = 'CM1000000'
    #     formatted_reference = create_formatted_payment_reference(test_cm_reference)
    #     more_prefix_in_payment_reference = formatted_reference[:4]
    #     reference_in_payment_reference = formatted_reference[5:14]
    #     timestamp_date = formatted_reference[15:23]
    #
    #     # Reference should include MORE prefix, full reference number, two colons and a yyyymmddhhmmss timestamp
    #     self.assertEqual(len(formatted_reference), 29)
    #     self.assertEqual('MORE', more_prefix_in_payment_reference)
    #     self.assertEqual(test_cm_reference, reference_in_payment_reference)
    #     self.assertEqual(timestamp_date, time.strftime("%Y%m%d"))
