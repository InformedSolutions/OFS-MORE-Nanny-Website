from django.test import TestCase
from django.urls import resolve, reverse

from tasks_app.views import TaskListView

from childcare_training_task_app import views
from childcare_training_task_app import forms


class LoginTests(TestCase):

    def test_can_render_guidance_page(self):
        """
        Test to assert that the 'Childcare-Training-Guidance' page can be rendered.
        """
        response = self.client.get(reverse('Childcare-Training-Guidance'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingGuidanceView)

    def test_can_render_type_of_childcare_page(self):
        """
        Test to assert that the 'Type-Of-Childcare-Training' page can be rendered.
        """
        response = self.client.get(reverse('Type-Of-Childcare-Training'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.TypeOfChildcareTrainingFormView)

    def test_can_render_childcare_training_course_page(self):
        """
        Test to assert that the 'Childcare-Training-Course' page can be rendered.
        """
        response = self.client.get(reverse('Childcare-Training-Course'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingCourseView)

    def test_can_render_childcare_training_summary_page(self):
        """
        Test to assert that the 'Childcare-Training-Summary' page can be rendered.
        """
        response = self.client.get(reverse('Childcare-Training-Summary'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingSummaryView)

    def test_post_request_to_guidance_page_redirects_correctly(self):
        """
         Test to assert that clicking 'Continue' on the guidance page takes you to the
         'Type-Of-Childcare-Training' page.
        """
        response = self.client.post(reverse('Childcare-Training-Summary'))
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, TaskListView)

    def test_post_request_to_childcare_training_course_redirects_to_task_list(self):
        """
        Test to assert that clicking 'Continue' on the guidance page takes you back to the task list.
        """
        response = self.client.post(reverse('Childcare-Training-Course'))
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingCourseView)

    def test_can_select_level_2_training(self):
        """
        Test to assert that the applicant can select 'Level 2 Training Course'.
        """
        response = self.client.post(reverse('Childcare-Training-Course'),
                                    {'childcare_training': 'level_2_training'})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingSummaryView)

    def test_can_select_common_core_training(self):
        """
        Test to assert that the applicant can select 'Common core training'.
        """
        response = self.client.post(reverse('Childcare-Training-Course'),
                                    {'childcare_training': 'common_core_training'})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingSummaryView)

    def test_can_select_no_training(self):
        """
        Test to assert that the applicant can select 'No training'.
        """
        response = self.client.post(reverse('Childcare-Training-Course'),
                                    {'childcare_training': 'no_training'})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingSummaryView)

    def can_select_both_level_2_and_common_core_training(self):
        """
        Test to assert that the applicant can select 'Level 2 Training Course' and 'Common core training'.
        """
        response = self.client.post(reverse('Childcare-Training-Course'),
                                    {'childcare_training': ['level_2_training', 'common_core_training']})
        found = resolve(response.request.get('PATH_INFO'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.ChildcareTrainingSummaryView)

    def test_cannot_select_none_with_another_option(self):
        """
        Test to assert that the applicant cannot select both 'No training' and another option.
        """
        option_combinations = [
            ['level_2_training', 'no_training'],
            ['common_core_training', 'no_training'],
            ['level_2_training', 'common_core_training', 'no_training']
        ]

        for combo in option_combinations:
            response = self.client.post(reverse('Childcare-Training-Course'),
                                        {'childcare_training': combo})
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.TypeOfChildcareTrainingFormView)
            self.assertFormError(response, 'form', 'childcare_training', 'Please select types of courses or none')
