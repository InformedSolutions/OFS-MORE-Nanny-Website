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

    '''
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
        self.assertEqual(found.func.view_class, views.ExistingUserSignInFormView)

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
            ('', 'Please enter an email address'),
            ('t', 'Please enter a valid email address, like yourname@example.com'),
            ('123', 'Please enter a valid email address, like yourname@example.com'),
            ('knights@ni', 'Please enter a valid email address, like yourname@example.com'),
        )

        for email, error in test_invalid_emails:
            response = self.client.post(reverse('New-User-Sign-In'), {'email_address': email})
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.NewUserSignInFormView)
            self.assertFormError(response, 'form', 'email_address', error)

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
            ('', 'Please enter an email address'),
            ('t', 'Please enter a valid email address, like yourname@example.com'),
            ('123', 'Please enter a valid email address, like yourname@example.com'),
            ('knights@ni', 'Please enter a valid email address, like yourname@example.com'),
        )

        for email, error in test_invalid_emails:
            response = self.client.post(reverse('Existing-User-Sign-In'), {'email_address': email})
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.ExistingUserSignInFormView)
            self.assertFormError(response, 'form', 'email_address', error)

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

    def test_security_code_page_can_be_rendered(self):
        """
        Test that the 'Security-Code' page can be rendered.
        """
        response = self.client.get(reverse('Security-Code'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.SecurityCodeFormView)

        # TODO: Test that the user details sms_expiry is updated.

    def test_invalid_sms_code_form_error_messages(self):
        """
        Test that invalid security codes reload same page with appropriate error messages raised.
        """
        codes_errors = (
            ('', 'Please enter the 5 digit code we sent to your mobile'),
            ('1', 'The code must be 5 digits. You have entered fewer than 5 digits'),
            ('123456', 'The code must be 5 digits. You have entered more than 5 digits'),
            # ('', ''),  # TODO: Add incorrect security code test.
        )

        for code, error in codes_errors:
            response = self.client.post(reverse('Security-Code'), {'sms_code': code})
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.SecurityCodeFormView)
            self.assertFormError(response, 'form', 'sms_code', error)

    def test_valid_sms_code_redirects_correctly(self):
        """
        Test that entering a correct SMS code redirects the user to the appropriate page.
        """
        # code = Identity-Gateway API call
        response = self.client.post(reverse('Security-Code'), {'sms_code': code})
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        # self.assertEqual(found.func.view_class, views.TaskListView)

    def test_can_render_link_used_page(self):
        """
        Test that the 'Link-Used' page can be rendered.
        """
        response = self.client.get(reverse('Link-Used'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.LinkUsedView)

    def test_can_render_application_saved_page(self):
        """
        Test that the 'Application-Saved' page can be rendered.
        """
        response = self.client.get(reverse('Application-Saved'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.ApplicationSavedView)

    def test_can_render_phone_number_page(self):
        """
        Test that the 'Phone-Number' page can be loaded.
        """
        response = self.client.get(reverse('Phone-Number'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)

    def test_can_add_mobile_number(self):
        """
        Test that a valid mobile number entered on the 'Phone-Number' page is saved.
        """
        response = self.client.post(reverse('Phone-Number'),
                                    {'mobile_number': '07754000000',
                                     'other_phone_number': ''})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.SummaryView)
        # TODO: Add API calls before and after to check phone number has been added to the application.


    def test_can_add_both_mobile_and_other_phone_number(self):
        """
        Test that entering valid numbers on the 'Phone-Number' page saves both.
        """
        response = self.client.post(reverse('Phone-Number'),
                                    {'mobile_number': '07754000000',
                                     'other_phone_number': '07754000000'})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.SummaryView)
        # TODO: Add API calls before and after to check both numbers have been added to the application.

    def test_invalid_mobile_number_validation_messages(self):
        """
        Test that invalid mobile numbers throw an error with the appropriate message.
        """
        number_errors = (
            ('', 'Please enter a mobile number'),
            ('1', 'Please enter a valid mobile number'),
            ('123456', 'Please enter a valid mobile number'),
        )

        for number, error in number_errors:
            response = self.client.post(reverse('Phone-Number'),
                                        {'mobile_number': number,
                                         'other_phone_number': ''})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)
        self.assertFormError(response, 'form', 'mobile_number', error)

    def test_invalid_other_phone_number_validation_messages(self):
        """
        Test that invalid other phone numbers throw an error with the appropriate message.
        """
        number_errors = (
            ('1', 'Please enter a valid phone number'),
            ('123456', 'Please enter a valid phone number'),
        )

        for number, error in number_errors:
            response = self.client.post(reverse('Phone-Number'),
                                        {'mobile_number': '07754000000',
                                         'other_phone_number': number})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)
        self.assertFormError(response, 'form', 'other_phone_number', error)

    def test_other_number_can_be_left_blank(self):
        """
        Test that other number can be blank and won't throw an error during validation.
        """
        response = self.client.post(reverse('Phone-Number'),
                                    {'mobile_number': '',
                                     'other_phone_number': ''})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)

        # self.assertFieldOutput('other_phone_number', valid=True)
        self.assertEqual(False, 'other_phone_number' in response.context_data['form'].errors)

    def test_can_render_resend_sms_code_page(self):
        """
        Test that the 'Resend-Security-Code' page can be rendered.
        """
        response = self.client.get(reverse('Resend-Security-Code'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.ResendSecurityCodeView)

    def test_resend_security_code_updates_user_details_and_redirects(self):
        """
        Test that clicking 'Send new code' on 'Resend-Security-Code' page updates the user's security code and redirects
        back to the 'Security-Code' page.
        """
        response = self.client.post(reverse('Resend-Security-Code'))
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.SecurityCodeFormView)
        # TODO: Make API call before and after to check that the account's security code has changed.
'''
