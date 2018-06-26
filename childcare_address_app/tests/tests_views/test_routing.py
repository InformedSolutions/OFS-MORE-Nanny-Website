from ..tests import ChildcareAddressTests, authenticate
from ...views import *
from django.urls import resolve
from unittest import mock
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class RoutingTests(ChildcareAddressTests):

    def test_service_unavailable_resolves_to_page(self):
        """
        Test to assert that the 'service unavailable' page can be rendered.
        """
        found = resolve(reverse('Service-Unavailable'))
        self.assertEqual(found.func.__name__, ServiceUnavailableView.__name__)

    def test_guidance_url_resolves_to_page(self):
        """
        Test to assert that the 'guidance' page can be rendered.
        """
        found = resolve(reverse('Childcare-Address-Guidance'))
        self.assertEqual(found.func.__name__, GuidanceView.__name__)

    def test_childcare_location_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Location'))
        self.assertEqual(found.func.__name__, ChildcareLocationView.__name__)


    def test_details_later_url_resolves_to_page(self):
        found = resolve(reverse('Childcare-Address-Details-Later'))
        self.assertEqual(found.func.__name__, AddressDetailsLaterView.__name__)
