from ..test_base import *
from django.urls import resolve
from ...views.guidance import *


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class GuidanceTests(InsuranceCoverTests):

    def test_guidance_url_resolves_to_page(self):
        """
        Test to assert that the url for the 'guidance' page can be resolved.
        """
        found = resolve(reverse('insurance:Guidance'))
        self.assertEqual(found.func.__name__, GuidanceView.__name__)

    def test_can_render_guidance_page(self):
        """
        Test to assert that the guidance page can be rendered
        """

        response = self.client.get(build_url('insurance:Guidance', get={
            'id': self.application_id
        }))

        self.assertEqual(response.status_code, 200)
