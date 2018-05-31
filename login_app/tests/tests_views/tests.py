from django.test import TestCase
from django.urls import reverse


class LoginTests(TestCase):

    def test_can_render_service_unavailable(self):
        """
        A simple example test to assert the 'service unavailable' page can be rendered
        """
        response = self.client.get(reverse('Service-Unavailable'))

        self.assertEqual(response.status_code, 200)
