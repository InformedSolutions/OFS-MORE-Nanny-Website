from django.core.signing import Signer
from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie
import uuid

from application.services.db_gateways import IdentityGatewayActions


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id):
    record = {
            'application_id': application_id,
            'email': 'test@informed.com'
        }
    return CustomResponse(record)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class TaskListTestsAuth(TestCase):
    application_id = uuid.UUID
    sample_app = {
        'application_id': application_id
    }

    def setUp(self):
        signer = Signer()
        signed_email = signer.sign('test@informed.com')
        self.client.cookies = SimpleCookie({'_ofs': signed_email})
