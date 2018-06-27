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
class PersonalDetailsTests(TestCase):

    sample_app = {
        'address_to_be_provided': True
    }

    sample_pd = {
        'first_name': 'TestFirst',
        'middle_names': None,
        'last_name': 'TestLast',
        'date_of_birth': None
            }

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
