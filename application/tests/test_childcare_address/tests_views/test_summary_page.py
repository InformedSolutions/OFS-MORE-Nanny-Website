from ..tests import ChildcareAddressTests, authenticate
from application.presentation.childcare_address.views import *
from django.urls import resolve
from unittest import mock
import uuid

from application.tests.test_utils import side_effect, side_effect_childcare_address_list

from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class ManualEntryTests(ChildcareAddressTests):

    def test_summary_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Summary'))
        self.assertEqual(found.func.__name__, ChildcareAddressSummaryView.__name__)

    def test_can_render_summary_page(self):
        """
        Test to assert that the summary page can be rendered.
        """
        self.skipTest('FIXME')
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.side_effect = side_effect
            nanny_api_list.side_effect = side_effect_childcare_address_list

            response = self.client.get(build_url('Childcare-Address-Summary', get={
                'id': self.sample_app['application_id']
            }))

            self.assertEqual(response.status_code, 200)
