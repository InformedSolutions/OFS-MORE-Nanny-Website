from uuid import uuid4

from django.shortcuts import reverse
from django.test import Client, modify_settings, TestCase
from django.urls import resolve

from dbs_app import forms, views


@modify_settings(MIDDLEWARE={
        'remove': [
            'middleware.CustomAuthenticationHandler',
        ]
    })
class CriminalRecordChecksTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_id = str(uuid4())

    def setUp(self):
        self.client = Client()

    # ------------------------------- #
    # Test View routing and rendering #
    # ------------------------------- #

    def test_can_render_guidance_page(self):
        response = self.client.get(reverse('dbs:Criminal-Record-Checks-Guidance-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.CriminalRecordsCheckGuidanceView)

    def test_post_request_to_guidance_page_redirects_to_lived_abroad_page(self):
        response = self.client.post('dbs:Guidance-View')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.LivedAbroadFormView)

    def test_post_request_to_guidance_page_sets_task_status_to_started(self):
        self.skipTest('NotImplemented')

    def test_can_render_lived_abroad_page(self):
        response = self.client.get(reverse('dbs:Lived-Abroad-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.LivedAbroadFormView)

    def test_no_to_lived_abroad_redirects_to_dbs_guidance_page(self):
        self.skipTest('NotImplemented')

    def test_yes_to_lived_abroad_redirects_to_certificates_of_good_conduct_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_certificates_of_good_conduct_page_redirects_to_post_good_conduct_certificates_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_post_good_conduct_certificates_page(self):
        response = self.client.get(reverse('dbs:Good-Conduct-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.GoodConductView)

    def test_post_request_to_post_good_conduct_certificates_page_redirects_to_dbs_guidance(self):
        # TODO: Check this doesn't involve an actual form.
        self.skipTest('NotImplemented')

    def test_can_render_dbs_guidance_page(self):
        response = self.client.get(reverse('dbs:DBS-Guidance-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.DBSGuidanceView)

    def test_post_request_to_dbs_guidance_page_redirects_to_dbs_type_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_dbs_type_page(self):
        response = self.client.get(reverse('dbs:DBS-Type-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.DBSTypeFormView)

    def test_capita_dbs_to_dbs_type_page_redirects_to_capita_dbs_details_page(self):
        self.skipTest('NotImplemented')

    def test_non_capita_dbs_to_dbs_type_page_redirects_to_dbs_update_service_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_capita_dbs_details_page(self):
        response = self.client.get(reverse('dbs:Capita-DBS-Details-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.CaptitaDBSDetailsFormView)

    def test_cautions_and_convictions_on_capita_dbs_details_page_redirects_to_post_dbs_certificate_page(self):
        self.skipTest('NotImplemented')

    def test_no_cautions_and_convicitons_on_capita_dbs_details_page_redirects_to_summmary_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_post_dbs_certificate_page(self):
        response = self.client.get(reverse('dbs:Post-DBS-Certificate'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.PostDBSCertificateView)

    def test_post_request_to_post_dbs_certificate_page_redirects_to_summary_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_dbs_update_service_page(self):
        response = self.client.get(reverse('dbs:DBS-Update-Service-Page'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.DBSUpdateServiceFormView)

    def test_yes_to_dbs_update_serice_page_redirects_to_non_capita_dbs_details_page(self):
        self.skipTest('NotImplemented')

    def test_no_to_dbs_update_page_redirects_to_get_a_dbs_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_get_a_dbs_page(self):
        response = self.client.get(reverse('dbs:Get-A-DBS-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.GetDBSView)

    def test_post_request_to_get_a_dbs_page_redirects_to_task_list(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_get_a_dbs_page_sets_task_status_to_started(self):
        self.skipTest('NotImplemented')

    def test_can_render_non_captita_dbs_details_page(self):
        response = self.client.get(reverse('dbs:Non-Captia-DBS-Details-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.NonCatitaDBSDetailsFormView)

    def test_post_to_non_captita_dbs_details_page_redirects_to_post_dbs_certificate_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_summary_page(self):
        response = self.client.get(reverse('dbs:Criminal-Record-Check-Summary-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.CriminalRecordChecksSummaryView)

    def test_post_request_to_summary_page_redirects_to_task_list(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_summary_page_sets_task_status_to_completed(self):
        self.skipTest('NotImplemented')

    # ---------- #
    # Test forms #
    # ---------- #

    def test_non_12_digit_dbs_raises_error(self):
        self.skipTest('NotImplemented')

    def test_not_entering_a_dbs_number_rasies_error(self):
        self.skipTest('NotImplemented')

    def test_not_entering_an_option_for_lived_abroad_raises_error(self):
        self.skipTest('NotImplemented')

    def test_not_entering_an_option_for_on_update_raises_error(self):
        self.skipTest('NotImplemented')

    def test_not_entering_an_option_for_dbs_type_raises_error(self):
        self.skipTest('NotImplemented')

    def test_not_declaring_to_post_certificates_of_good_conduct_raises_error(self):
        self.skipTest('NotImplemented')

    def test_not_entering_cautions_and_convictions_raises_error(self):
        self.skipTest('NotImplemented')
