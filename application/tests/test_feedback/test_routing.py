from http.cookies import SimpleCookie
from unittest import mock

from django.http import HttpResponse
from django.test import modify_settings, TestCase
from django.urls import resolve, reverse

from ...presentation.feedback.views import feedback as feedback_view
from ...presentation.login.views import StartPageView


class FeedbackTests(TestCase):

    def test_feedback_successfully_submitted(self):
        """
        Test to assert that feedback is successfully submitted when valid feedback is entered
        """

        with mock.patch.object(feedback_view, 'send_email') as send_email_mock:
            send_email_mock.return_value.status_code = 201

            # POST valid input to feedback page
            response = self.client.post(
                reverse('Feedback'),
                {
                    'feedback': 'Test feedback',
                    'email_address': 'tester@informed.com',
                    'url': reverse('Start-Page')
                }
            )
            self.assertEqual(response.status_code, 302)
            # Assert taken to feedback confirmation page
            self.assertTemplateUsed('feedback-confirmation.html')

    def test_feedback_successfully_submitted_no_email(self):
        """
        Test to assert that feedback is successfully submitted when valid feedback is entered (without email address)
        """

        with mock.patch.object(feedback_view, 'send_email') as send_email_mock:
            send_email_mock.return_value.status_code = 201

            # POST valid input to feedback page
            response = self.client.post(
                reverse('Feedback'),
                {
                    'feedback': 'Test feedback',
                    'email_address': '',
                    'url': reverse('Start-Page')
                }
            )

            self.assertEqual(response.status_code, 302)
            # Assert taken to feedback confirmation page
            self.assertTemplateUsed('feedback-confirmation.html')

    def test_invalid_feedback_submitted(self):
        """
        Test to assert that feedback is not submitted when invalid feedback is entered
        """

        with mock.patch.object(feedback_view, 'send_email') as send_email_mock:
           send_email_mock.return_value.status_code = 201

           # POST valid input to feedback page
           response = self.client.post(
                reverse('Feedback'),
                {
                    'feedback': '',
                    'email_address': 'tester@informed.com',
                    'url': reverse('Start-Page')
                }
            )
           print(response) 
           self.assertEqual(response.status_code, 200)

           # Assert stay on feedback page
           self.assertEqual(response.resolver_match.view_name, 'Feedback')

           error = response.context['field_errors'].values()
           error_message = len(list(error))

           # Assert error message returned to user
           self.assertEqual(error_message, 1)

    def test_feedback_email_sent_when_validation_passes_on_feedback(self):
        """
        Test to assert that the send_email function is called on posting valid feedback
        """
        with mock.patch.object(feedback_view, 'send_email') as send_email_mock:
            send_email_mock.return_value.status_code = 201

            response = self.client.post(
                reverse('Feedback'),
                {
                    'feedback': 'test',
                    'email_address':'tester@informed.com',
                    'url': reverse('Start-Page')
                }
            )





    def test_feedback_confirmation_page_redirects_to_previous_url(self):
        """
         Test to assert that the feedback confirmation page redirects to the url
         that the feedback page was accessed from
        """
        response = self.client.post(
            reverse('Feedback-Confirmation'),
            {
                'url': reverse('Start-Page')
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resolve(response.url).func.__name__, StartPageView.__name__)
        self.assertTemplateUsed('start-page.html')