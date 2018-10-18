import os
from unittest import mock

from django.test import TestCase, tag
from django.urls import resolve, reverse
from nanny.db_gateways import NannyGatewayActions

from nanny.test_utils import side_effect, mock_nanny_application, mock_personal_details_record, mock_identity_record
from login_app import views


class YourChildrenTests(TestCase):

    def setUp(self):
        self.user_details_record = mock_identity_record

        self.nanny_application_record = mock_nanny_application

        self.personal_details_record = mock_personal_details_record

        self.nanny_actions = NannyGatewayActions()

    def test_can_access_your_children_endpoint(self):
        """
        Test to assert that the 'your_children' endpoint can be accessed.
        """

        response = self.nanny_actions.list('application', params={})

        self.assertEqual(response.status_code, 200)