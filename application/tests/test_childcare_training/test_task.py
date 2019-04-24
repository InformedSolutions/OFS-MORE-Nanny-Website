from unittest import mock

from http.cookies import SimpleCookie

from django.core.signing import TimestampSigner
from django.test import TestCase, modify_settings
from django.urls import resolve, reverse

from application.tests.test_utils import side_effect
from application.presentation.task_list.views import TaskListView
from application.presentation.childcare_training import views
from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions


@modify_settings(MIDDLEWARE={
        'remove': [
            'middleware.CustomAuthenticationHandler',
        ]
    })
class ChildcareTrainingTests(TestCase):

    def setUp(self):
        self.application_id = 'ef78049d-40fb-4808-943c-593fa3a9700b'
        signer = TimestampSigner()
        signed_email = signer.sign('test@informed.com')
        self.client.cookies = SimpleCookie({'_ofs': signed_email})
        self.application_record = {
            'application_id': self.application_id,
            'childcare_training_status': 'NOT_STARTED',
        }
        self.childcare_training_record = {
            'level_2_training': False,
            'common_core_training': False,
            'no_training': False
        }

    def test_can_render_guidance_page(self):
        """
        Test to assert that the 'Childcare-Training-Guidance' page can be rendered.
        """
        with mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('Childcare-Training-Guidance') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.ChildcareTrainingGuidanceView)

    def test_can_render_certificate_page(self):
        """
        Test to assert that the 'Childcare-Training-Certificate' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:

            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('Childcare-Training-Certificate') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.ChildcareTrainingCertificateView)

    def test_can_render_type_of_childcare_page(self):
        """
        Test to assert that the 'Type-Of-Childcare-Training' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(NannyGatewayActions, 'list'):

            nanny_api_get.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('Type-Of-Childcare-Training') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.TypeOfChildcareTrainingFormView)

    def test_can_render_childcare_training_course_page(self):
        """
        Test to assert that the 'Childcare-Training-Course' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions,'read') as identity_api_read:

            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('Childcare-Training-Course') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.ChildcareTrainingCourseView)

    def test_can_render_childcare_training_summary_page(self):
        """
        Test to assert that the 'Childcare-Training-Summary' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(NannyGatewayActions, 'list'):

            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('Childcare-Training-Summary') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.ChildcareTrainingSummaryView)

    def test_post_request_to_guidance_page_redirects_correctly(self):
        """
         Test to assert that clicking 'Continue' on the guidance page takes you to the
         'Type-Of-Childcare-Training' page.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put:

            nanny_api_get.return_value.record = self.application_record
            nanny_api_put.return_value.status_code = 200

            response = self.client.post(reverse('Childcare-Training-Summary') + '?id=' + self.application_id)
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, TaskListView)

    def test_post_request_to_childcare_training_course_redirects_to_task_list(self):
        """
        Test to assert that clicking 'Continue' on the guidance page takes you back to the task list.
        """
        response = self.client.post(reverse('Childcare-Training-Course') + '?id=' + self.application_id)
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, TaskListView)

    def test_can_select_level_2_training(self):
        """
        Test to assert that the applicant can select 'Level 2 Training Course'.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as training_api_get, \
                mock.patch.object(NannyGatewayActions, 'put') as training_api_put, \
                mock.patch.object(NannyGatewayActions, 'list'):

            training_api_get.return_value.status_code = 200
            training_api_get.return_value.record = self.childcare_training_record
            training_api_put.return_value.status_code = 200

            response = self.client.post(reverse('Type-Of-Childcare-Training') + '?id=' + self.application_id,
                                        {'childcare_training': 'level_2_training'})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.ChildcareTrainingCertificateView)

    def test_can_select_common_core_training(self):
        """
        Test to assert that the applicant can select 'Common core training'.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as training_api_get, \
                mock.patch.object(NannyGatewayActions, 'put') as training_api_put, \
                mock.patch.object(NannyGatewayActions, 'list'):

            training_api_get.return_value.status_code = 200
            training_api_get.return_value.record = self.childcare_training_record
            training_api_put.return_value.status_code = 200

            response = self.client.post(reverse('Type-Of-Childcare-Training') + '?id=' + self.application_id,
                                        {'childcare_training': {'common_core_training': True}})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.ChildcareTrainingCertificateView)

    def test_can_select_no_training(self):
        """
        Test to assert that the applicant can select 'No training'.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as training_api_get, \
                mock.patch.object(NannyGatewayActions, 'put') as training_api_put, \
                mock.patch.object(NannyGatewayActions, 'list'):

            training_api_get.return_value.status_code = 200
            training_api_get.return_value.record = self.childcare_training_record
            training_api_put.return_value.status_code = 200

            response = self.client.post(reverse('Type-Of-Childcare-Training') + '?id=' + self.application_id,
                                        {'childcare_training': 'no_training'})
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(found.func.view_class, views.ChildcareTrainingCourseView)

    def can_select_both_level_2_and_common_core_training(self):
        """
        Test to assert that the applicant can select 'Level 2 Training Course' and 'Common core training'.
        """
        response = self.client.post(reverse('Type-Of-Childcare-Training') + '?id=' + self.application_id,
                                    {'childcare_training': ['level_2_training', 'common_core_training']})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingSummaryView)

    def test_cannot_select_none_with_another_option(self):
        """
        Test to assert that the applicant cannot select both 'No training' and another option.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as training_api_get, \
                mock.patch.object(NannyGatewayActions, 'list'):

            training_api_get.return_value.status_code = 404

            option_combinations = [
                ['level_2_training', 'no_training'],
                ['common_core_training', 'no_training'],
                ['level_2_training', 'common_core_training', 'no_training']
            ]

            for combo in option_combinations:
                response = self.client.post(reverse('Type-Of-Childcare-Training') + '?id=' + self.application_id,
                                            {'childcare_training': combo})

                view_class_name = response.resolver_match._func_path
                class_ = getattr(globals()['views'], view_class_name.split('.')[-1])

                self.assertEqual(response.status_code, 200)
                self.assertEqual(class_, views.TypeOfChildcareTrainingFormView)
                self.assertFormError(response, 'form', 'childcare_training', 'Please select types of courses or none')
