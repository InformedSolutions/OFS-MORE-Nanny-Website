from django.test import TestCase, tag, Client
from django.urls import reverse, resolve

from django.test import modify_settings


@modify_settings(MIDDLEWARE={
    'remove': [
        'nanny.middleware.CustomAuthenticationHandler',
    ]
})
class YourLocationRoutingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('Your-Location')

    @tag('http')
    def test_manual_entry_url_resolves_to_page(self):
        from application.presentation.login.views.your_location import your_location

        found = resolve(reverse('Your-Location'))
        self.assertEqual(found.func.__name__, your_location.__name__)

    @tag('http')
    def test_can_render_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @tag('http')
    def test_invalid_post_empty_data(self):
        data = {}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    @tag('http')
    def test_invalid_post_blank_data(self):
        data = {'your_location': None}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    @tag('http')
    def test_valid_post_true(self):
        data = {'your_location': True}
        expected_redirect_page_name = 'Account-Selection'

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(expected_redirect_page_name))

    @tag('http')
    def test_valid_post_false(self):
        data = {'your_location': False}
        expected_redirect_url = 'https://online.ofsted.gov.uk/onlineofsted/Ofsted_Online.ofml'

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_redirect_url)
