from ..tests import authenticate, YourChildrenTests
from django.urls import resolve, reverse
from unittest import mock
from ...views import *
import uuid
from django.template.response import TemplateResponse

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class SummaryTest(YourChildrenTests):

    def test_name_resolves_to_page(self):
        found = resolve(reverse('your-children:Your-Children-Summary'))
        self.assertCountEqual(found.func.__name__, YourChildrenSummaryView.__name__)

    def test_can_render_summary_page(self):
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('your-children:Your-Children-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_summary_page(self):
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(
                build_url('your-children:Your-Children-Summary', get={'id': str(uuid.uuid4())}),
                data=
                {
                    'id': uuid.uuid4(),
                }
            )

            self.assertEqual(response.status_code, 302)
            self.assertTrue('task-list/' in response.url)
