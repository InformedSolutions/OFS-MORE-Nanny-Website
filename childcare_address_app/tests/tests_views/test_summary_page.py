from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from unittest import mock
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class ManualEntryTests(ChildcareAddressTests):

    def test_summary_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Summary'))
        self.assertEqual(found.func.__name__, ChildcareAddressSummaryView.__name__)

    def test_can_render_summary_page(self):
        """
        Test to assert that the summary page can be rendered.
        """

        with mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get_app, \
                mock.patch('nanny_models.childcare_address.ChildcareAddress.api.get_records') as nanny_api_get_addresses, \
                mock.patch('nanny_models.applicant_home_address.ApplicantHomeAddress.api.get_record') as nanny_api_get_home_address:
            app_id = uuid.UUID
            self.sample_app['application_id'] = app_id
            self.sample_address['application_id'] = app_id
            self.sample_address['childcare_address_id'] = uuid.UUID
            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app

            nanny_api_get_addresses.return_value.status_code = 200
            nanny_api_get_addresses.return_value.record = [self.sample_address]

            nanny_api_get_home_address.return_value.status_code = 200
            nanny_api_get_home_address.return_value.record = {'childcare_address': True}

            response = self.client.get(build_url('Childcare-Address-Summary', get={
                'id': app_id
            }))

            self.assertEqual(response.status_code, 200)