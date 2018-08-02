import uuid

from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie

from nanny.test_utils import mock_nanny_application, mock_dbs_record


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


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class DBSTests(TestCase):
    """
    Base class from which the remainder of the DBS tests inherit from
    """

    # These are the only fields acted on by the API requests in these tests, therefore are the only ones written
    sample_dbs = mock_dbs_record

    sample_app = mock_nanny_application

    def setUp(self):
        """
        Defines the authentication cookie for use in DBS tests
        """
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})