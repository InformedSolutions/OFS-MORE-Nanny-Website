from django.test import TestCase
from django.urls import reverse


class ExampleTests(TestCase):

    def test_can_render_template_page(self):
        """
        A simple example test to assert the index page for the template can be rendered
        :return:
        """
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
