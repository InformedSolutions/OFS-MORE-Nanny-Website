from ..test_base import *
from django.urls import resolve
from ...views.insurance_cover import *

@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class InsuranceCoverTests(InsuranceCoverTests):

    def test_insurance_cover_url_resolves_to_page(self):
        """
        Test to assert that the url for the 'insurance cover' page can be resolved.
        """
        found = resolve(reverse('insurance:Insurance-Cover'))
        self.assertEqual(found.func.__name__, InsuranceCoverView.__name__)

    def test_can_render_insurance_cover_page(self):
        """
        Test to assert that the insurance cover page can be rendered
        """

        response = self.client.get(build_url('insurance:Insurance-Cover', get={
            'id': self.application_id
        }))

        self.assertEqual(response.status_code, 200)
