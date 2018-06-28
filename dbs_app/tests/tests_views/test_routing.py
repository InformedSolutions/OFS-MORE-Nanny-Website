from ..tests import DBSTests, authenticate
from ...views import *
from django.urls import resolve
from unittest import mock
import uuid


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class RoutingTests(DBSTests):

    def test_guidance_url_resolves_to_page(self):
        """
        Test to assert that the 'guidance' page can be rendered.
        """
        found = resolve(reverse('dbs:Guidance'))
        self.assertEqual(found.func.__name__, DBSGuidance.__name__)

    def test_details_url_resolves_to_page(self):
        """
        Test to assert that the 'details' page can be rendered.
        """
        found = resolve(reverse('dbs:Details'))
        self.assertEqual(found.func.__name__, DBSDetailsView.__name__)

    def test_dbs_upload_url_resolves_to_page(self):
        """
        Test to assert that the 'dbs upload' page can be rendered.
        """
        found = resolve(reverse('dbs:DBS-Upload'))
        self.assertEqual(found.func.__name__, DBSUpload.__name__)

    def test_summary_url_resolves_to_page(self):
        """
        Test to assert that the 'summary' page can be rendered.
        """
        found = resolve(reverse('dbs:Summary'))
        self.assertEqual(found.func.__name__, DBSSummary.__name__)

