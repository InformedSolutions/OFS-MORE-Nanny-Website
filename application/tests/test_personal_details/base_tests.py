from django.test import TestCase, modify_settings
from unittest import mock
from http.cookies import SimpleCookie
import uuid

from application.services.db_gateways import IdentityGatewayActions

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


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
@modify_settings(MIDDLEWARE={
        'remove': [
            'nanny.middleware.CustomAuthenticationHandler',
        ]
    })
class PersonalDetailsTests(TestCase):

    sample_app = {
        'address_to_be_provided': True
    }

    sample_pd = {
        'personal_detail_id': uuid.UUID,
        'first_name': 'TestFirst',
        'middle_names': None,
        'last_name': 'TestLast',
        'date_of_birth': '1997-08-23',
        'lived_abroad': False,
        'your_children': True
            }

    sample_addr = {
        'street_line1': 'Test',
        'street_line2': None,
        'town': 'Test Town',
        'county': None,
        'postcode': 'WA14 4PA'
    }

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
