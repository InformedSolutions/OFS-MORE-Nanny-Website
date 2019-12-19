from django.test import TestCase, tag, Client
from django.urls import reverse, resolve

from django.test import modify_settings


@modify_settings(MIDDLEWARE={
    'remove': [
        'nanny.middleware.CustomAuthenticationHandler',
    ]
})
class AccountSelectionRoutingTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('Account-Selection')

    @tag('http')
    def test_manual_entry_url_resolves_to_page(self):
        from application.presentation.login.views.account_selection import AccountSelectionFormView

        found = resolve(reverse('Account-Selection'))
        self.assertEqual(found.func.__name__, AccountSelectionFormView.__name__)

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





