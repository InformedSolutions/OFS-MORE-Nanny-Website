from ..test_base import TaskListTestsAuth, authenticate
from unittest import mock
from django.urls import resolve
from application.presentation.task_list.views import *
from application.presentation.utilities import *


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class CostTests(TaskListTestsAuth):

    def test_can_resolve_costs_page(self):
        found = resolve(reverse('Costs'))
        self.assertEqual(found.func.__name__, CostsView.__name__)

    def test_can_render_costs_page(self):
        response = self.client.get(build_url('Costs', get={
            'id': self.application_id
        }))

        self.assertEqual(response.status_code, 200)
