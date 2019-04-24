from django.core.signing import TimestampSigner
from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie

from application.tests.test_utils import mock_home_address, mock_nanny_application, mock_identity_record

from application.services.db_gateways import IdentityGatewayActions


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id, *args, **kwargs):
    record = mock_identity_record
    return CustomResponse(record)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class ChildcareAddressTests(TestCase):

    sample_app = mock_nanny_application

    sample_address = mock_home_address

    def setUp(self):
        signer = TimestampSigner()
        signed_email = signer.sign('test@informed.com')
        self.client.cookies = SimpleCookie({'_ofs': signed_email})
