from uuid import uuid4

from django.forms import ValidationError
from django.shortcuts import reverse
from django.test import Client, modify_settings, TestCase
from django.urls import resolve

from dbs_app import forms as dbs_forms#, views
from tasks_app.views import TaskListView


@modify_settings(MIDDLEWARE={
        'remove': [
            'middleware.CustomAuthenticationHandler',
        ]
    })
class CriminalRecordChecksTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CriminalRecordChecksTest, cls).setUpClass()
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
        self.assertTemplateUsed('criminal-record-checks-guidance.html')

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
        self.assertTemplateUsed('lived-abroad.html')

    def test_no_to_lived_abroad_redirects_to_dbs_guidance_page(self):
        response = self.client.post(reverse('dbs:Lived-Abroad-View'), data={'lived_abroad': False})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, views.DBSGuidanceView)

    def test_yes_to_lived_abroad_redirects_to_certificates_of_good_conduct_page(self):
        response = self.client.post(reverse('dbs:Lived-Abroad-View'), data={'lived_abroad': True})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, views.GoodConductView)

    def test_post_request_to_certificates_of_good_conduct_page_redirects_to_post_good_conduct_certificates_page(self):
        response = self.client.post(reverse('dbs:Good-Conduct-View'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, views.GoodConductView)

    def test_can_render_post_good_conduct_certificates_page(self):
        response = self.client.get(reverse('dbs:Good-Conduct-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.PostGoodConductCertificatesView)
        self.assertTemplateUsed('post-good-conduct-certificates.html')

    def test_post_request_to_post_good_conduct_certificates_page_redirects_to_dbs_guidance(self):
        # TODO: Check this doesn't involve an actual form.
        self.skipTest('NotImplemented')

    def test_can_render_dbs_guidance_page(self):
        response = self.client.get(reverse('dbs:DBS-Guidance-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.DBSGuidanceView)
        self.assertTemplateUsed('dbs-guidance.html')

    def test_post_request_to_dbs_guidance_page_redirects_to_dbs_type_page(self):
        response = self.client.post(reverse('dbs:DBS-Guidance-View'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, views.DBSGuidanceView)

    def test_can_render_dbs_type_page(self):
        response = self.client.get(reverse('dbs:DBS-Type-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.DBSTypeFormView)
        self.assertTemplateUsed('dbs-type.html')

    def test_capita_dbs_to_dbs_type_page_redirects_to_capita_dbs_details_page(self):
        response = self.client.post(reverse('dbs:DBS-Type-View'), data={'is_ofsted_dbs': True})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, views.CaptitaDBSDetailsFormView)

    def test_non_capita_dbs_to_dbs_type_page_redirects_to_dbs_update_service_page(self):
        response = self.client.post(reverse('dbs:DBS-Type-View'), data={'is_ofsted_dbs': False})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, views.DBSUpdateServiceFormView)

    def test_can_render_capita_dbs_details_page(self):
        response = self.client.get(reverse('dbs:Capita-DBS-Details-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.CaptitaDBSDetailsFormView)
        self.assertTemplateUsed('capita-dbs-details.html')

    def test_cautions_and_convictions_on_capita_dbs_details_page_redirects_to_post_dbs_certificate_page(self):
        self.skipTest('NotImplemented')

    def test_no_cautions_and_convicitons_on_capita_dbs_details_page_redirects_to_summmary_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_post_dbs_certificate_page(self):
        response = self.client.get(reverse('dbs:Post-DBS-Certificate'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.PostDBSCertificateView)
        self.assertTemplateUsed('post-dbs-certificate.html')

    def test_post_request_to_post_dbs_certificate_page_redirects_to_summary_page(self):
        response = self.client.post(reverse('dbs:Post-DBS-Certificate'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, CriminalRecordChecksSummaryView)

    def test_can_render_dbs_update_service_page(self):
        response = self.client.get(reverse('dbs:DBS-Update-Service-Page'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.DBSUpdateServiceFormView)
        self.assertTemplateUsed('dbs-update-service.html')

    def test_yes_to_dbs_update_serice_page_redirects_to_non_capita_dbs_details_page(self):
        self.skipTest('NotImplemented')

    def test_no_to_dbs_update_page_redirects_to_get_a_dbs_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_get_a_dbs_page(self):
        response = self.client.get(reverse('dbs:Get-A-DBS-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.GetDBSView)
        self.assertTemplateUsed('get-a-dbs.html')

    def test_post_request_to_get_a_dbs_page_redirects_to_task_list(self):
        response = self.client.post(reverse('dbs:Get-A-DBS-View'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).__name__, TaskListView)

    def test_post_request_to_get_a_dbs_page_sets_task_status_to_started(self):
        self.skipTest('NotImplemented')

    def test_can_render_non_captita_dbs_details_page(self):
        response = self.client.get(reverse('dbs:Non-Captia-DBS-Details-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.NonCatitaDBSDetailsFormView)
        self.assertTemplateUsed('non-capita-dbs-details.html')

    def test_post_to_non_captita_dbs_details_page_redirects_to_post_dbs_certificate_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_summary_page(self):
        response = self.client.get(reverse('dbs:Criminal-Record-Check-Summary-View'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.__name__, views.CriminalRecordChecksSummaryView)
        self.assertTemplateUsed('criminal-record-checks-summary.html')

    def test_post_request_to_summary_page_redirects_to_task_list(self):
        response = self.client.post(reverse('dbs:Criminal-Record-Check-Summary-View'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.__name__, TaskListView)

    def test_post_request_to_summary_page_sets_task_status_to_completed(self):
        self.skipTest('NotImplemented')

    # ---------- #
    # Test forms #
    # ---------- #

    def test_less_than_12_digit_dbs_raises_error(self):
        form = dbs_forms.NonCapitaDBSDetailsForm(data={'dbs_number': '1'})

        with self.assertRaisesMessage(ValidationError, 'Check your certificate: the number should be 12 digits long'):
            form.clean_dbs_number()

    def test_more_than_12_digit_dbs_raises_error(self):
        form = dbs_forms.NonCapitaDBSDetailsForm(data={'dbs_number': '0000000000013'})

        with self.assertRaisesMessage(ValidationError, 'Check your certificate: the number should be 12 digits long'):
            form.clean_dbs_number()

    def test_not_entering_a_dbs_number_rasies_error(self):
        form = dbs_forms.NonCapitaDBSDetailsForm(data={'dbs_number': ''})

        with self.assertRaisesMessage(ValidationError, 'Please enter your DBS certificate number'):
            form.fields['dbs_number'].clean()

    def test_entering_a_12_digit_dbs_number_does_not_raise_error(self):
        form = dbs_forms.NonCapitaDBSDetailsForm(data={'dbs_number': '012345678912'})

        self.assertTrue(form.is_valid())

    def test_not_entering_an_option_for_lived_abroad_raises_error(self):
        form = dbs_forms.LivedAbroadForm(data={'lived_abroad': ''})

        with self.assertRaisesMessage(ValidationError, 'Please say if you have lived outside of the UK in the last 5 years'):
            form.fields['lived_abroad'].clean('')

    def test_not_entering_an_option_for_on_update_raises_error(self):
        self.skipTest('NotImplemented')

    def test_not_entering_an_option_for_dbs_type_raises_error(self):
        form = dbs_forms.DBSTypeForm(data={'is_ofsted_dbs': ''})

        with self.assertRaisesMessage(ValidationError, 'Please say if you have an Ofsted DBS check'):
            form.fields['is_ofsted_dbs'].clean('')

    def test_not_declaring_to_post_certificates_of_good_conduct_raises_error(self):
        self.skipTest('NotImplemented')

    def test_not_entering_cautions_and_convictions_raises_error(self):
        form = dbs_forms.CaptiaDBSDetailsForm(data={'has_convictions': ''})

        with self.assertRaisesMessage(ValidationError, 'Please say if you have any criminal cautions or convictions'):
            form.fields['has_convictions'].clean('')
