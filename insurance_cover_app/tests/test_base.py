from ...nanny.utilities import *
from django.test import TestCase
from unittest import mock
from http.cookies import SimpleCookie
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class InsuranceCoverTests(TestCase):
    application_id = None

    sample_app = {
        'application_id': application_id
    }

    def setUp(self):
        self.application_id = uuid.UUID
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
