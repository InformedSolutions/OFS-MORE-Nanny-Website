from ...nanny.utilities import *
from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie
import uuid


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


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class InsuranceCoverTests(TestCase):
    application_id = None

    sample_app = {
        'application_id': application_id
    }

    def setUp(self):
        self.application_id = uuid.UUID
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
