from django.test import TestCase
from django.urls import resolve, reverse

from login_app import views


class LoginTests(TestCase):

    def test_can_render_service_unavailable(self):
        """
        Test to assert that the 'service unavailable' page can be rendered.
        """
        response = self.client.get(reverse('Service-Unavailable'))

        self.assertEqual(response.status_code, 200)

    def test_can_render_accout_selection_page(self):
        """
        Test to assert that the 'Account-Selection' page can be rendered.
        """
        response = self.client.get(reverse('Account-Selection'))

        self.assertEqual(response.status_code, 200)

    def test_empty_account_selection_form_redirects_to_self(self):
        """
        Test to assert that not selecting an option on the 'Account-Selection' redirects back to the same page.
        """
        response = self.client.post(reverse('Account-Selection'), {'account_selection': None})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.AccountSelectionFormView)

    def test_can_select_new_application(self):
        """
        Test to assert that selecting 'Return to application' on the 'Account-Selection' page redirects to appropriate
        page.
        """
        response = self.client.post(reverse('Account-Selection'), {'account_selection': 'new'})
        # found = resolve(response.request.get('url'))
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.NewUserSignInFormView)

    def test_can_select_existing_application(self):
        """
        Test to assert that selecting 'Return to application' on the 'Account-Selection' page redirects to appropriate
        page.
        """
        response = self.client.post(reverse('Account-Selection'), {'account_selection': 'existing'})

        self.assertEqual(response.status_code, 302)
        # TODO : Assert exactly which page the client should land on.

    def test_can_render_new_user_sign_in_page(self):
        """
        Test to assert that the 'New-User-Sign-In' page can be rendered.
        """
        response = self.client.get(reverse('New-User-Sign-In'))

        self.assertEqual(response.status_code, 200)

    def test_invalid_email_redirects_to_self(self):
        """
        Test that entering an invalid email on the 'New-User-Sign-In' page redirects back to the same page.
        """
        test_invalid_emails = (
            '',
            't',
            '123',
            'knights@ni'
        )

        for email in test_invalid_emails:
            response = self.client.post(reverse('New-User-Sign-In'), {'email_address': email})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.NewUserSignInFormView)

    def test_valid_email_address_creates_account_and_redirects(self):
        """
        Test that entering a valid email address on the 'New-User-Sign-In' page creates an account with that email and
        redirects to the appropriate page.
        """
        response = self.client.post(reverse('New-User-Sign-In'), {'email_address': 'eva@walle.com'})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        # self.assertEqual(found.func.view_class, views.CheckEmailView)

        #TODO - Assert response codes from Identity API for queries before and after POST request with valid email.
