import uuid

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
class DBSTests(TestCase):

    sample_dbs = {
        'dbs_number': 123456789012,
        'convictions': 'False',
    }

    sample_app = {
        'application_id': str(uuid.uuid4()),
        'criminal_record_check_status': 'NOT_STARTED'
    }

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})