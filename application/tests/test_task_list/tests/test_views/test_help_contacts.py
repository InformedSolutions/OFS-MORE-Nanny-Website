from ..test_base import TaskListTestsAuth, authenticate
from unittest import mock
from django.urls import resolve
from application.presentation.task_list.views import *
from application.presentation.utilities import *


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class HelpContactTests(TaskListTestsAuth):

    def test_can_resolve_help_contact_page(self):
        found = resolve(reverse('Help-And-Contact'))
        self.assertEqual(found.func.__name__, HelpAndContactView.__name__)

    def test_can_render_help_contact_page(self):
        response = self.client.get(build_url('Help-And-Contact', get={
            'id': self.application_id
        }))

        self.assertEqual(response.status_code, 200)
