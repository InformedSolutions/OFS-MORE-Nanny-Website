from unittest import mock
from uuid import uuid4

from django.forms import ValidationError
from django.shortcuts import reverse
from django.test import Client, modify_settings, SimpleTestCase, TestCase
from django.urls import resolve

from application.presentation.dbs import forms as dbs_forms, views
from application.services.db_gateways import NannyGatewayActions
from application.tests.test_utils import side_effect
from application.presentation.task_list.views import TaskListView
from django.http import HttpResponse


@modify_settings(MIDDLEWARE={
        'remove': [
            'nanny.middleware.CustomAuthenticationHandler',
        ]
    })
@mock.patch.object(NannyGatewayActions, 'create', side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'read',   side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'list',   side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'patch',  side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'put',    side_effect=side_effect)
@mock.patch.object(NannyGatewayActions, 'delete', side_effect=side_effect)
class CriminalRecordChecksTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CriminalRecordChecksTest, cls).setUpClass()
        cls.app_id = str(uuid4())
        cls.url_suffix = '?id=' + cls.app_id

    def setUp(self):
        self.client = Client()

    # ------------------------------- #
    # Test View routing and rendering #
    # ------------------------------- #

    def test_can_render_guidance_page(self, *args):
        response = self.client.get(reverse('dbs:Criminal-Record-Checks-Guidance-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.CriminalRecordsCheckGuidanceView.__name__)
        self.assertTemplateUsed('criminal-record-checks-guidance.html')

    def test_post_request_to_guidance_page_redirects_to_lived_abroad_page(self, *args):
        response = self.client.post(reverse('dbs:Criminal-Record-Checks-Guidance-View') + self.url_suffix)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.LivedAbroadFormView.__name__)

    def test_post_request_to_guidance_page_sets_task_status_to_in_progress(self, *args):
        self.client.post(reverse('dbs:Criminal-Record-Checks-Guidance-View') + self.url_suffix)
        patch_mock = args[2]

        self.assertTrue(patch_mock.called)
        patch_mock.assert_called_once_with('application', params={'application_id': self.app_id, 'dbs_status': 'IN_PROGRESS'})

    def test_can_render_lived_abroad_page(self, *args):
        response = self.client.get(reverse('dbs:Lived-Abroad-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.LivedAbroadFormView.__name__)
        self.assertTemplateUsed('lived-abroad.html')

    def test_no_to_lived_abroad_redirects_to_dbs_guidance_page(self, *args):
        response = self.client.post(reverse('dbs:Lived-Abroad-View') + self.url_suffix, data={'lived_abroad': False})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.DBSGuidanceView.__name__)

    def test_yes_to_lived_abroad_redirects_to_criminal_records_abroad_page(self, *args):
        response = self.client.post(reverse('dbs:Lived-Abroad-View') + self.url_suffix, data={'lived_abroad': True})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.CriminalRecordsFromAbroadView.__name__)

    def can_render_criminal_records_abroad_page(self, *args):
        response = self.client.get(reverse('dbs:Criminal-Records-Abroad-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.CriminalRecordsFromAbroadView.__name__)
        self.assertTemplateUsed('criminal-record-abroad.html')

    def test_criminal_records_abroad_page_contains_link_to_email_good_conduct_certificates_page(self, *args):
        response = self.client.get(reverse('dbs:Criminal-Records-Abroad-View') + self.url_suffix)

        expected_link = reverse('dbs:Email-Good-Conduct-Certificates-View') + self.url_suffix

        self.assertContains(response, '<a href="%s" class="button">Continue</a>' % expected_link, html=True)

    def test_can_render_email_good_conduct_certificates_page(self, *args):
        response = self.client.get(reverse('dbs:Email-Good-Conduct-Certificates-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.EmailGoodConductCertificatesView.__name__)
        self.assertTemplateUsed('email-good-conduct-certificates.html')

    def test_post_good_conduct_certificates_page_contains_link_to_dbs_guidance_page(self, *args):
        response = self.client.get(reverse('dbs:Email-Good-Conduct-Certificates-View') + self.url_suffix)

        expected_link = reverse('dbs:DBS-Guidance-View') + self.url_suffix

        self.assertContains(response, '<a href="%s" class="button">Continue</a>' % expected_link, html=True)

    def test_can_render_dbs_guidance_page(self, *args):
        response = self.client.get(reverse('dbs:DBS-Guidance-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.DBSGuidanceView.__name__)
        self.assertTemplateUsed('dbs-guidance.html')

    def test_dbs_guidance_page_contains_link_to_dbs_details_page(self, *args):
        response = self.client.get(reverse('dbs:DBS-Guidance-View') + self.url_suffix)

        expected_link = reverse('dbs:Capita-DBS-Details-View') + self.url_suffix

        self.assertContains(response, '<a href="%s" class="button">Continue</a>' % expected_link, html=True)

    def test_can_render_capita_dbs_details_page(self, *args):
        response = self.client.get(reverse('dbs:Capita-DBS-Details-View') + self.url_suffix)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.CapitaDBSDetailsFormView.__name__)
        self.assertTemplateUsed('capita-dbs-details.html')

    def test_capita_dbs_details_no_capita_redirect(self, *args):
        from application.presentation.dbs.forms import dbs_details as form_dbs
        from application.presentation.dbs.views import capita_dbs_details as view_dbs

        http_response = HttpResponse()
        http_response.status_code = 404

        with mock.patch.object(form_dbs, 'read_dbs') as mock_form_read:
            with mock.patch.object(view_dbs, 'read_dbs') as mock_view_read:
                mock_form_read.return_value = http_response
                mock_view_read.return_value = http_response

                response = self.client.post(reverse('dbs:Capita-DBS-Details-View') + self.url_suffix, data={'dbs_number':'123456789101'})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(resolve(response.url).func.__name__, views.DBSTypeFormView.__name__)


    def test_can_render_post_dbs_certificate_page(self, *args):
        response = self.client.get(reverse('dbs:Post-DBS-Certificate') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.PostDBSCertificateView.__name__)
        self.assertTemplateUsed('post-dbs-certificate.html')

    def test_post_dbs_certificate_page_contains_link_to_summary_page(self, *args):
        response = self.client.get(reverse('dbs:Post-DBS-Certificate') + self.url_suffix)

        expected_link = reverse('dbs:Criminal-Record-Check-Summary-View') + self.url_suffix

        self.assertContains(response, '<a href="%s" class="button">Continue</a>' % expected_link, html=True)

    def test_can_render_dbs_update_service_page(self, *args):
        response = self.client.get(reverse('dbs:DBS-Update-Service-Page') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.DBSUpdateServiceFormView.__name__)
        self.assertTemplateUsed('dbs-update-service.html')

    def test_yes_to_dbs_update_serice_page_redirects_to_non_capita_dbs_details_page(self, *args):
        response = self.client.post(reverse('dbs:DBS-Update-Service-Page') + self.url_suffix,
                                    data={
                                        'on_dbs_update_service': True
                                    })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.NonCapitaDBSDetailsFormView.__name__)

    def test_can_render_non_captita_dbs_details_page(self, *args):
        response = self.client.get(reverse('dbs:Non-Capita-DBS-Details-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.NonCapitaDBSDetailsFormView.__name__)
        self.assertTemplateUsed('non-capita-dbs-details.html')

    def test_can_render_summary_page(self, *args):
        response = self.client.get(reverse('dbs:Criminal-Record-Check-Summary-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.CriminalRecordChecksSummaryView.__name__)
        self.assertTemplateUsed('criminal-record-checks-summary.html')

    def test_post_request_to_summary_page_redirects_to_task_list(self, *args):
        response = self.client.post(reverse('dbs:Criminal-Record-Check-Summary-View') + self.url_suffix)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, TaskListView.__name__)

    def test_post_request_to_summary_page_sets_task_status_to_completed(self, *args):
        self.client.post(reverse('dbs:Criminal-Record-Check-Summary-View') + self.url_suffix)
        patch_mock = args[2]

        self.assertTrue(patch_mock.called)
        patch_mock.assert_called_once_with('application', params={'application_id': self.app_id, 'dbs_status': 'COMPLETED'})

    def test_get_request_to_apply_page_sets_task_status_to_started(self, *args):
        self.client.get(reverse('dbs:DBS-Apply-View') + self.url_suffix)
        patch_mock = args[2]
        print(patch_mock.called)
        self.assertTrue(patch_mock.called)
        patch_mock.assert_called_once_with('application', params={'application_id': self.app_id, 'dbs_status': 'IN_PROGRESS'})

    def test_get_request_to_sign_up_page_sets_task_status_to_started(self, *args):
        self.client.get(reverse('dbs:DBS-Sign-Up-View') + self.url_suffix)
        patch_mock = args[2]
        print(patch_mock.called)

        self.assertTrue(patch_mock.called)
        patch_mock.assert_called_once_with('application', params={'application_id': self.app_id, 'dbs_status': 'IN_PROGRESS'})

    def test_can_render_dbs_type_page(self, *args):
        response = self.client.get(reverse('dbs:DBS-Type-View') + self.url_suffix)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.DBSTypeFormView.__name__)
        self.assertTemplateUsed('dbs-type.html')

    def test_dbs_type_no_redirect_if_no_data(self, *args):
        response = self.client.post(reverse('dbs:DBS-Type-View') + self.url_suffix, data={'enhanced_check':'', 'on_dbs_update_service': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.DBSTypeFormView.__name__)
        self.assertTemplateUsed('dbs-type.html')

    def test_dbs_type_no_redirect_if_enhanced_yes_data(self, *args):
        response = self.client.post(reverse('dbs:DBS-Type-View') + self.url_suffix, data={'enhanced_check': True})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.DBSTypeFormView.__name__)
        self.assertTemplateUsed('dbs-type.html')

    def test_dbs_type_no_capita_yes_yes_redirect(self, *args):
        response = self.client.post(reverse('dbs:DBS-Type-View') + self.url_suffix,
                                    data={'enhanced_check': True, 'on_dbs_update_service': True})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.DBSUpdateCheckView.__name__)
        self.assertTemplateUsed('dbs-update-check.html')

    def test_dbs_type_no_capita_yes_no_redirect(self, *args):
        response = self.client.post(reverse('dbs:DBS-Type-View') + self.url_suffix,
                                    data={'enhanced_check': True, 'on_dbs_update_service': False})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.DBSSignUpView.__name__)
        self.assertTemplateUsed('dbs-sign-up.html')

    def test_dbs_apply_redirect_to_task_list(self, *args):
        response = self.client.post(reverse('dbs:DBS-Apply-View') + self.url_suffix)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.TaskList.__name__)

    def test_dbs_sign_up_redirect_to_task_list(self, *args):
        response = self.client.post(reverse('dbs:DBS-Sign-Up-View') + self.url_suffix)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.TaskList.__name__)

    def test_dbs_sign_up_redirect_to_task_list(self, *args):
        response = self.client.post(reverse('dbs:DBS-Update-Check-View') + self.url_suffix)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, views.CriminalRecordCheckSummaryView.__name__)














