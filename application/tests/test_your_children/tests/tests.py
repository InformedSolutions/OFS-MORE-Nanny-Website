from http.cookies import SimpleCookie
from unittest import mock
import uuid
from django.test import TestCase
from application.services.db_gateways import NannyGatewayActions
from application.tests.test_utils import mock_nanny_application, mock_personal_details_record, mock_identity_record


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id, *args, **kwargs):
    record={
        'application_id': application_id,
        'id': application_id,
        'email': 'test@informed.com'
    }
    return CustomResponse(record)


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class YourChildrenTests(TestCase):

    def setUp(self):
        self.user_details_record = mock_identity_record
        self.nanny_application_record = mock_nanny_application
        self.personal_details_record = mock_personal_details_record
        self.nanny_actions = NannyGatewayActions()
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})

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