from ..test_base import TaskListTestsAuth, authenticate
from unittest import mock
from django.urls import resolve
from ...views import *
from ...utils import *


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class HelpContactTests(TaskListTestsAuth):

    def test_can_resolve_help_contact_page(self):
        found = resolve(reverse('Help-And-Contact'))
        self.assertEqual(found.func.__name__, HelpAndContactView.__name__)

    def test_can_render_help_contact_page(self):
        response = self.client.get(build_url('Help-And-Contact', get={
            'id': self.application_id
        }))

        self.assertEqual(response.status_code, 200)
