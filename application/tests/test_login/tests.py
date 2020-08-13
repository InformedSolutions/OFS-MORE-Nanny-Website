import os
from unittest import mock

from django.core.signing import TimestampSigner
from django.http import HttpRequest, SimpleCookie
from django.test import TestCase
from django.urls import resolve, reverse

from application.tests.test_utils import side_effect, mock_nanny_application, mock_personal_details_record, mock_identity_record
from application.presentation.login import views

from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions
from application.services import notify
from application.presentation import utilities


class LoginTests(TestCase):

    def setUp(self):
        self.user_details_record = mock_identity_record

        self.nanny_application_record = mock_nanny_application

        self.personal_details_record = mock_personal_details_record

        signer = TimestampSigner()
        signed_email = signer.sign('test@informed.com')
        self.client.cookies = SimpleCookie({'_ofs': signed_email})

    def test_can_render_service_unavailable(self):
        """
        Test to assert that the 'service unavailable' page can be rendered.
        """
        response = self.client.get(reverse('Service-Unavailable'))

        self.assertEqual(response.status_code, 200)

    def test_can_render_account_selection_page(self):
        """
        Test to assert that the 'Account-Selection' page can be rendered.
        """
        response = self.client.get(reverse('Account-Selection'))

        self.assertEqual(response.status_code, 200)

    def test_empty_account_selection_form_redirects_to_self(self):
        """
        Test to assert that not selecting an option on the 'Account-Selection' redirects back to the same page.
        """
        response = self.client.post(reverse('Account-Selection'), {'account_selection': ''})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.AccountSelectionFormView)
        self.assertFormError(response, 'form', 'account_selection', 'Please select one')

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

    def test_service_down_page_shown_if_test_notify_fails(self):
        """
        Test that a user is redirected to the 'Service-Unavailable' page if test_notify() returns false during either
        the new user of existing user login.
        """
        with mock.patch.object(utilities, 'test_notify') as test_notify:
            test_notify.return_value = False

            views_to_test = (
                'New-User-Sign-In',
                'Existing-User-Sign-In',
            )

            for view in views_to_test:
                response = self.client.post(reverse(view), {'email_address': 'eva@walle.com'})
                found = resolve(response.url)

                self.assertEqual(response.status_code, 302)
                self.assertEqual(found.func.view_class, views.ServiceUnavailableView)

    def test_valid_new_email_address_creates_account_and_redirects(self):
        """
        Test that entering a valid email address on the 'New-User-Sign-In' page creates an account with that email and
        redirects to the appropriate page.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
            mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(reverse('New-User-Sign-In'), {'email_address': 'eva@walle.com'})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.CheckEmailView)

    def test_check_email_page_can_be_rendered(self):
        """
        Test that the check email pages can be rendered and that it contains a link to the 'Resend-Email' page.
        """
        check_email_pages = ('Check-New-Email', 'Check-Existing-Email')  # Check both the 'Check-Email' pages.
        for page in check_email_pages:
            response = self.client.get(reverse(page) + '?email_address=' + self.user_details_record['email'])
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.CheckEmailView)
            self.assertContains(
                response,
                '<a href="{}">resend the email</a>'.format(reverse('Resend-Email') + '?email_address=' + self.user_details_record['email']),
                html=True
            )

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
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(notify, 'send_email') as notify_email:

            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect


            response = self.client.post(reverse('Existing-User-Sign-In'), {'email_address': 'eva@walle.com'})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.CheckEmailView)

    def test_email_sent_with_with_valid_email_upon_sign_in(self):
        """
        Check that notify-gateway send_email function us called when valid email entered on both the 'New-User-Sign-In'
        and 'Existing-User-Sign-In' pages.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(notify, 'send_email') as notify_email:

            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect

            check_email_pages = ('New-User-Sign-In', 'Existing-User-Sign-In')  # Check both the 'Check-Email' pages.

            for page in check_email_pages:
                self.client.post(reverse(page), {'email_address': 'eva@walle.com'})

                self.assertTrue(notify_email.called)

    def test_resend_email_page_can_be_rendered(self):
        """
        Test that the 'Resend-Email' page can be rendered and that it contains a link to the 'Help-And-Contacts' page.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(IdentityGatewayActions, 'list') as identity_api_list, \
                mock.patch.object(notify, 'send_email') as notify_email:

            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect

            identity_api_list.return_value.status_code = 200
            identity_api_list.return_value.record = [self.user_details_record]

            response = self.client.get(reverse('Resend-Email') + '?email_address=' + self.user_details_record['email'])

            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response,
                '<a href="{}">contact Ofsted</a>'.format(reverse('Help-And-Contacts')),
                html=True
            )

    def test_email_sent_when_rendering_resend_email_page(self):
        """
        Test that notify.send_email() is called during rendering of the 'Resend-Email' page.
        """
        with mock.patch.object(IdentityGatewayActions, 'list') as identity_api_list, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(notify, 'send_email') as notify_email:

            identity_api_list.return_value.record = [self.user_details_record]
            identity_api_put.side_effect = side_effect

            self.client.get(reverse('Resend-Email'), {'email_address': 'eva@walle.com'})

            self.assertTrue(notify_email.called)

    def test_validating_email_magic_link_redirects_to_sms_page_for_existing_applicant(self):
        """
        Test that the returning user who navigates to the link sent via email is then redirected to the SMS page.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(IdentityGatewayActions, 'list') as identity_api_list, \
                mock.patch.object(notify, 'send_text') as notify_send_text, \
                mock.patch.object(views.ValidateMagicLinkView, 'link_has_expired') as link_expired:

            identity_api_list.return_value.record = [self.user_details_record]
            identity_api_list.return_value.status_code = 200
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect
            link_expired.return_value = False

            response = self.client.get(os.environ.get('PUBLIC_APPLICATION_URL') + '/validate/'
                                       + self.user_details_record['magic_link_email'] + '/')
            found = resolve(response.url)

            self.assertEqual(302, response.status_code)
            self.assertEqual(found.func.view_class, views.SecurityCodeFormView)

    def test_cookie_update_after_magic_link(self):
        """
        Test that the returning user's cookie updates to match their email address for their session
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(IdentityGatewayActions, 'list') as identity_api_list, \
                mock.patch.object(notify, 'send_text') as notify_send_text, \
                mock.patch.object(views.ValidateMagicLinkView, 'link_has_expired') as link_expired:

            identity_api_list.return_value.record = [self.user_details_record]
            identity_api_list.return_value.status_code = 200
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect
            link_expired.return_value = False
            email = self.user_details_record['email']

            self.client.get(os.environ.get('PUBLIC_APPLICATION_URL') + '/validate/' + self.user_details_record['magic_link_email'] + '/')
            cookie = self.client.cookies['_ofs'].value

            signer = TimestampSigner()
            signed_email = signer.sign(email)

            self.assertEqual(cookie, signed_email)

    def test_validating_email_magic_link_sends_sms(self):
        """
        Test that the returning user who navigates to the link sent via email is then sent an SMS.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(IdentityGatewayActions, 'list') as identity_api_list, \
                mock.patch.object(notify, 'send_text') as notify_send_text, \
                mock.patch.object(views.ValidateMagicLinkView, 'link_has_expired') as link_expired:

            identity_api_list.return_value.record = [self.user_details_record]
            identity_api_list.return_value.status_code = 200
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect
            link_expired.return_value = False

            self.client.get(os.environ.get('PUBLIC_APPLICATION_URL') + '/validate/'
                            + self.user_details_record['magic_link_email'] + '/')

            self.assertTrue(notify_send_text.called)

    def test_security_code_page_can_be_rendered(self):
        """
        Test that the 'Security-Code' page can be rendered.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put:
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect

            response = self.client.get(reverse('Security-Code') + '?id=' + self.user_details_record['application_id'])
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.SecurityCodeFormView)

    def test_invalid_sms_code_form_error_messages(self):
        """
        Test that invalid security codes reload same page with appropriate error messages raised.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get:
            identity_api_get.side_effect = side_effect

            codes_errors = (
                ('', 'Please enter the 5 digit code we sent to your mobile'),
                ('1', 'The code must be 5 digits. You have entered fewer than 5 digits'),
                ('123456', 'The code must be 5 digits. You have entered more than 5 digits'),
                ('23456', 'Invalid code. Check the code we sent to your mobile.'),  # Incorrect security code test.
            )

            for code, error in codes_errors:
                response = self.client.post(
                    reverse('Security-Code') + '?id=' + self.user_details_record['application_id'],
                    {'sms_code': code},
                )
                found = resolve(response.request.get('PATH_INFO'))

                self.assertEqual(response.status_code, 200)
                self.assertEqual(found.func.view_class, views.SecurityCodeFormView)
                self.assertFormError(response, 'form', 'sms_code', error)


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
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put:
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect

            response = self.client.get(reverse('Phone-Number') + '?id=' + self.user_details_record['application_id'])
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)

    def test_can_add_mobile_number(self):
        """
        Test that a valid mobile number entered on the 'Phone-Number' page is saved.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
                mock.patch.object(views.ValidateMagicLinkView, 'link_has_expired') as link_expired:

            identity_api_get.side_effect = side_effect

            nanny_api_get.return_value.record = {
                'application_status': 'DRAFTING',
                'login_details_status': 'COMPLETED',
            }
            identity_api_get.return_value.record = self.user_details_record
            link_expired.return_value = False

            response = self.client.post(reverse('Phone-Number') + '?id=' + self.user_details_record['application_id'],
                                        {'mobile_number': '07754000000',
                                         'other_phone_number': ''})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.ContactDetailsSummaryView)

    def test_can_add_both_mobile_and_other_phone_number(self):
        """
        Test that entering valid numbers on the 'Phone-Number' page saves both.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
                mock.patch.object(views.ValidateMagicLinkView, 'link_has_expired') as link_expired:

            identity_api_get.side_effect = side_effect

            nanny_api_get.return_value.record = {
                'application_status': 'DRAFTING',
                'login_details_status': 'COMPLETED',
            }
            identity_api_get.return_value.record = self.user_details_record
            link_expired.return_value = False

            response = self.client.post(reverse('Phone-Number') + '?id=' + self.user_details_record['application_id'],
                                        {'mobile_number': '07754000000',
                                         'other_phone_number': '07754000000'})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.ContactDetailsSummaryView)

    def test_invalid_mobile_number_validation_messages(self):
        """
        Test that invalid mobile numbers throw an error with the appropriate message.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
                mock.patch.object(views.ValidateMagicLinkView, 'link_has_expired') as link_expired:

            identity_api_get.side_effect = side_effect

            number_errors = (
                ('', 'Please enter a mobile number'),
                ('1', 'Please enter a valid mobile number'),
                ('123456', 'Please enter a valid mobile number'),
                ('123456789012', 'Please enter a valid mobile number'),
            )

            for number, error in number_errors:
                response = self.client.post(
                    reverse('Phone-Number') + '?id=' + self.user_details_record['application_id'],
                    {'mobile_number': number, 'other_phone_number': ''}
                )
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)
            self.assertFormError(response, 'form', 'mobile_number', error)

    def test_invalid_other_phone_number_validation_messages(self):
        """
        Test that invalid other phone numbers throw an error with the appropriate message.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
                mock.patch.object(views.ValidateMagicLinkView, 'link_has_expired') as link_expired:

            identity_api_get.side_effect = side_effect
            link_expired  = False

            number_errors = (
                ('1', 'Please enter a valid phone number'),
                ('123456', 'Please enter a valid phone number'),
                ('123456789012', 'Please enter a valid phone number'),
            )

            for number, error in number_errors:
                response = self.client.post(
                    reverse('Phone-Number') + '?id=' + self.user_details_record['application_id'],
                    {'mobile_number': '07754000000','other_phone_number': number}
                )
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)
            self.assertFormError(response, 'form', 'other_phone_number', error)

    def test_other_number_can_be_left_blank(self):
        """
        Test that other number can be blank and won't throw an error during validation.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put:
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect

            response = self.client.post(reverse('Phone-Number') + '?id=' + self.user_details_record['application_id'],
                                        {'mobile_number': '',
                                         'other_phone_number': ''})
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.PhoneNumbersFormView)

            self.assertEqual(False, 'other_phone_number' in response.context_data['form'].errors)

    def test_can_render_resend_sms_code_page(self):
        """
        Test that the 'Resend-Security-Code' page can be rendered.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put:
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect

            response = self.client.get(reverse('Resend-Security-Code') + '?id=' + self.user_details_record['application_id'])
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.ResendSecurityCodeView)

    def test_resend_security_code_updates_user_details_and_redirects(self):
        """
        Test that clicking 'Send new code' on 'Resend-Security-Code' page updates the user's security code and redirects
        back to the 'Security-Code' page.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put:
            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect

            response = self.client.post(reverse('Resend-Security-Code') + '?id=' + self.user_details_record['application_id'])
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.SecurityCodeFormView)

    def test_security_question_page_can_be_rendered(self):
        """
        Test to assert that the 'Security-Question' page can be rendered.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get, \
                mock.patch.object(IdentityGatewayActions, 'put') as identity_api_put, \
                mock.patch.object(IdentityGatewayActions, 'list') as identity_api_list, \
                mock.patch.object(NannyGatewayActions ,'read') as nanny_api_read:

            identity_api_list.return_value.record = [self.user_details_record]

            identity_api_get.side_effect = side_effect
            identity_api_put.side_effect = side_effect
            nanny_api_read.side_effect = side_effect

            response = self.client.get(reverse('Security-Question') + '?id=' + self.user_details_record['application_id'])
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.SecurityQuestionFormView)

    def test_login_redirect_helper_function_if_application_not_yet_created(self):
        """
        Test the behaviour of the login_redirect_helper_function in the case where an applicant has not yet
        completed their login details => has not created a NannyApplication object.
        Expect to land on the 'Contact-Details-Summary' page.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
            mock.patch.object(IdentityGatewayActions, 'read') as identity_api_get:

            nanny_get_response = mock.Mock()
            nanny_get_response.status_code = 404
            del nanny_get_response.record
            nanny_api_get.return_value = nanny_get_response
            identity_api_get.side_effect = side_effect

            response = self.client.post(
                reverse('Security-Code') + '?id=' + self.user_details_record['application_id'],
                {'sms_code': self.user_details_record['magic_link_sms']}
            )

            self.assertEqual(response.status_code, 302)
            self.assertEqual(resolve(response.url).func.view_class, views.ContactDetailsSummaryView)


    def test_can_render_cookie_page(self):
        """
        Test that the cookie page can render
        """
        response = self.client.get(reverse('Cookie-Policy'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.resolver_match.view_name, 'Cookie-Policy')

    def test_cookie_update_after_form_submission(self):
        form_data = {
            'cookie_selection': 'opted_in',
            'url': ''
        }
        self.client.get(reverse('Cookie-Policy'))
        response = self.client.post(reverse('Cookie-Policy'), form_data)
        self.assertEqual(response.cookies['cookie_preferences'].value, 'opted_in')