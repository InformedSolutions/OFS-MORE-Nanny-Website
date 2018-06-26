from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie


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


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class ChildcareAddressTests(TestCase):

    sample_app = {
        'address_to_be_provided': True
    }

    sample_address = {
                'street_line1': 'Test',
                'street_line2': None,
                'town': 'Test',
                'county': None,
                'postcode': 'WA14 4PA'
            }

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
