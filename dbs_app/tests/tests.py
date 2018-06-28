import uuid

from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id):
    """
    Authentication handler for middleware calls during tests
    :param application_id:
    :return: A mocked version of the authentication middleware response
    """
    record = {
            'application_id': application_id,
            'email': 'test@informed.com'
        }
    return CustomResponse(record)


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class DBSTests(TestCase):
    """
    Base class from which the remainder of the DBS tests inherit from
    """

    # These are the only fields acted on by the API requests in these tests, therefore are the only ones written
    sample_dbs = {
        'dbs_number': 123456789012,
        'convictions': 'False',
    }

    sample_app = {
        'application_id': str(uuid.uuid4()),
        'criminal_record_check_status': 'NOT_STARTED'
    }

    def setUp(self):
        """
        Defines the authentication cookie for use in DBS tests
        """
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})