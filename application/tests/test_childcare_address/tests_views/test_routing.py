from unittest import mock

from django.urls import resolve

from ..tests import ChildcareAddressTests, authenticate
from application.presentation.childcare_address.views import *

from application.services.db_gateways import IdentityGatewayActions


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class RoutingTests(ChildcareAddressTests):

    def test_guidance_url_resolves_to_page(self):
        """
        Test to assert that the 'guidance' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Guidance'))
        self.assertEqual(found.func.__name__, GuidanceView.__name__)

    def test_where_you_work_url_resolves_to_page(self):
        """
        Test to assert that the 'where you work' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Where-You-Work'))
        self.assertEqual(found.func.__name__, WhereYouWorkView.__name__)

    def test_details_later_url_resolves_to_page(self):
        """
        Test to assert that the 'details later' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Details-Later'))
        self.assertEqual(found.func.__name__, AddressDetailsLaterView.__name__)

    def test_childcare_location_url_resolves_to_page(self):
        """
        Test to assert that the 'childcare location' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Location'))
        self.assertEqual(found.func.__name__, ChildcareLocationView.__name__)

    def test_childcare_address_postcode_url_resolves_to_page(self):
        """
        Test to assert that the 'childcare address postcode' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Postcode-Entry'))
        self.assertEqual(found.func.__name__, ChildcareAddressPostcodeView.__name__)

    def test_childcare_address_lookup_url_resolves_to_page(self):
        """
        Test to assert that the 'childcare address lookup' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Lookup'))
        self.assertEqual(found.func.__name__, ChildcareAddressLookupView.__name__)

    def test_childcare_address_manual_url_resolves_to_page(self):
        """
        Test to assert that the 'childcare address manual entry' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Manual-Entry'))
        self.assertEqual(found.func.__name__, ChildcareAddressManualView.__name__)

    def test_childcare_address_summary_url_resolves_to_page(self):
        """
        Test to assert that the 'childcare address summary' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Summary'))
        self.assertEqual(found.func.__name__, ChildcareAddressSummaryView.__name__)
