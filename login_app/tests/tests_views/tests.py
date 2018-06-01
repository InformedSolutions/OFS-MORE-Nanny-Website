from django.test import TestCase
from django.urls import resolve, reverse

from login_app import views
from login_app import forms


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
        # self.assertFormError(response, forms.AcccountSelectionForm, field=account_selection)

    def test_can_select_new_application(self):
        """
        Test to assert that selecting 'Return to application' on the 'Account-Selection' page redirects to appropriate
        page.
        """
        response = self.client.post(reverse('Account-Selection'), {'account_selection': 'new'})
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.NewUserSignInFormView)

    def test_can_select_existing_application(self):
        """
        Test to assert that selecting 'Return to application' on the 'Account-Selection' page redirects to appropriate
        page.
        """
        response = self.client.post(reverse('Account-Selection'), {'account_selection': 'existing'})
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.ExistingUserSignIn)

    def test_can_render_new_user_sign_in_page(self):
        """
        Test to assert that the 'New-User-Sign-In' page can be rendered.
        """
        response = self.client.get(reverse('New-User-Sign-In'))

        self.assertEqual(response.status_code, 200)

    def test_invalid_new_user_email_redirects_to_self(self):
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
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.NewUserSignInFormView)
            # self.assertFormError(response, forms.ContactEmailForm, field=ContactEmailForm.email_address)

    def test_valid_new_email_address_creates_account_and_redirects(self):
        """
        Test that entering a valid email address on the 'New-User-Sign-In' page creates an account with that email and
        redirects to the appropriate page.
        """
        response = self.client.post(reverse('New-User-Sign-In'), {'email_address': 'eva@walle.com'})
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.CheckEmailView)

        # TODO - Assert response codes from Identity API for queries before and after POST request with valid email.

    def test_check_email_page_can_be_rendered(self):
        """
        Test that the check email pages can be rendered and that it contains a link to the 'Resend-Email' page.
        """
        check_email_pages = ('Check-New-Email', 'Check-Existing-Email')  # Check both the 'Check-Email' pages.
        for page in check_email_pages:
            response = self.client.get(reverse(page))
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.CheckEmailView)
            self.assertContains(response, '<a href="{}">resend the email</a>'.format(reverse('Resend-Email')), html=True)

    def test_can_render_existing_user_sign_in_page(self):
        """
        Test to assert that the 'New-User-Sign-In' page can be rendered.
        """
        response = self.client.get(reverse('Existing-User-Sign-In'))

        self.assertEqual(response.status_code, 200)

    def test_invalid_existing_user_email_redirects_to_self(self):
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
            response = self.client.post(reverse('Existing-User-Sign-In'), {'email_address': email})
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.ExistingUserSignIn)
            # self.assertFormError(response, forms.ContactEmailForm, field=ContactEmailForm.email_address)
            # self.assertFieldOutput()

    def test_valid_existing_email_address_loads_account_and_redirects(self):
        """
        Test that entering a valid email address on the 'New-User-Sign-In' page creates an account with that email and
        redirects to the appropriate page.
        """
        response = self.client.post(reverse('Existing-User-Sign-In'), {'email_address': 'eva@walle.com'})
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.CheckEmailView)

        # TODO - Assert response codes from Identity API for queries before and after POST request with valid email.

    def test_resend_email_page_can_be_rendered(self):
        """
        Test that the 'Resend-Email' page can be rendered and that it contains a link to the 'Help-And-Contacts' page.
        """
        response = self.client.post(reverse('Existing-User-Sign-In'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="{}">contact Ofsted</a>'.format(reverse('Help-And-Contacts')), html=True)

        # TODO - Assert response codes from Identity API before and after choosing to resend email validation link.
