from ..test_base import *
from django.urls import resolve
from ...views.summary import *

@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class SummaryTests(InsuranceCoverTests):

    def test_summary_url_resolves_to_page(self):
        """
        Test to assert that the url for the 'summary' page can be resolved.
        """
        found = resolve(reverse('insurance:Summary'))
        self.assertEqual(found.func.__name__, SummaryView.__name__)

    def test_can_render_summary_page(self):
        """
        Test to assert that the summary page can be rendered
        """
        with mock.patch('nanny_models.insurance_cover.InsuranceCover.api.get_record') as nanny_api_get:
            response = self.client.get(build_url('insurance:Summary', get={
                'id': self.application_id
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_post_to_summary_page(self):
        """
        Test to assert that the summary page can be rendered
        """
        with mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get_app, \
        mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_put_app:
            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app
            response = self.client.post(build_url('insurance:Summary', get={
                'id': self.application_id
            }))

            self.assertEqual(response.status_code, 302)
            self.assertTrue('task-list' in response.url)
