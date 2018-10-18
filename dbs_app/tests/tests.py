from django.test import modify_settings, TestCase


@modify_settings(MIDDLEWARE={
        'remove': [
            'middleware.CustomAuthenticationHandler',
        ]
    })
class CriminalRecordChecksTest(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    # ------------------------------- #
    # Test View routing and rendering #
    # ------------------------------- #

    def test_can_render_guidance_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_guidance_page_redirects_to_lived_abroad_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_guidance_page_sets_task_status_to_started(self):
        self.skipTest('NotImplemented')

    def test_can_render_lived_abroad_page(self):
        self.skipTest('NotImplemented')

    def test_no_to_lived_abroad_redirects_to_dbs_guidance_page(self):
        self.skipTest('NotImplemented')

    def test_yes_to_lived_abroad_redirects_to_certificates_of_good_conduct_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_certificates_of_good_conduct_page_redirects_to_post_good_conduct_certificates_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_post_good_conduct_certificates_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_post_good_conduct_certificates_page_redirects_to_dbs_guidance(self):
        # TODO: Check this doesn't involve an actual form.
        self.skipTest('NotImplemented')

    def test_can_render_dbs_guidance_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_dbs_guidance_page_redirects_to_dbs_type_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_dbs_type_page(self):
        self.skipTest('NotImplemented')

    def test_capita_dbs_to_dbs_type_page_redirects_to_capita_dbs_details_page(self):
        self.skipTest('NotImplemented')

    def test_non_capita_dbs_to_dbs_type_page_redirects_to_dbs_update_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_capita_dbs_details_page(self):
        self.skipTest('NotImplemented')

    def test_cautions_and_convictions_on_capita_dbs_details_page_redirects_to_post_dbs_certificate_page(self):
        self.skipTest('NotImplemented')

    def test_no_cautions_and_convicitons_on_capita_dbs_details_page_redirects_to_summmary_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_post_dbs_certificate_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_post_dbs_certificate_page_redirects_to_summary_page(self):
        self.skipTest('NotImplemented')

    def test_can_dbs_update_page(self):
        self.skipTest('NotImplemented')

    def test_yes_to_dbs_update_page_redirects_to_non_capita_dbs_details_page(self):
        self.skipTest('NotImplemented')

    def test_no_to_dbs_update_page_redirects_to_get_a_dbs_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_get_a_dbs_page(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_get_a_dbs_page_redirects_to_task_list(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_get_a_dbs_page_sets_task_status_to_started(self):
        self.skipTest('NotImplemented')

    def test_can_render_non_captita_dbs_details_page(self):
        self.skipTest('NotImplemented')

    def test_post_to_non_captita_dbs_details_page_redirects_to_post_dbs_certificate_page(self):
        self.skipTest('NotImplemented')

    def test_can_render_summary_page(self):
        self.skipTest('NotImplemented')

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
