from ..tests import ChildcareAddressTests, authenticate
from application.presentation.childcare_address.views import *
from django.urls import resolve, reverse
from unittest import mock

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
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list,\
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
            mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
            mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create:

            nanny_api_read.return_value.status_code = 200
            nanny_api_list.return_value.status_code = 200
            self.sample_address['childcare_address_id'] = '7e6f1bf3-ee36-444d-99c6-b521d51a484f'
            self.sample_address['endpoint_name'] = 'childcare-address'
            nanny_api_list.return_value.record = [self.sample_address]

            url_suffix = '?id=' + self.sample_app['application_id']

            response = self.client.get(reverse('Childcare-Address-Summary')+ url_suffix)

            self.assertEqual(response.status_code, 200)
