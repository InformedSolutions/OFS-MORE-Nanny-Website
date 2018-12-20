from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie

from nanny.test_utils import mock_home_address, mock_nanny_application, mock_identity_record


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id, *args, **kwargs):
    record = mock_identity_record
    return CustomResponse(record)


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class ChildcareAddressTests(TestCase):

    sample_app = mock_nanny_application

    sample_address = mock_home_address

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})