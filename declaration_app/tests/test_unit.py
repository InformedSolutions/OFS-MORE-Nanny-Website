from unittest import mock

from http.cookies import SimpleCookie

from django.test import TestCase, modify_settings
from django.urls import resolve, reverse

from declaration_app import views

from nanny.test_utils import side_effect


@modify_settings(MIDDLEWARE={
        'remove': [
            'middleware.CustomAuthenticationHandler',
        ]
    })
class DeclarationTests(TestCase):

    def setUp(self):
        self.application_id = 'ef78049d-40fb-4808-943c-593fa3a9700b'
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
        self.tasks = (
            'login_details_status',
            'personal_details_status',
            'childcare_address_status',
            'first_aid_training_status',
            'childcare_training_status',
            'criminal_record_check_status',
            'insurance_cover_status',
        )
        self.nanny_models = views.MasterSummary.model_names
        self.application_record = {
            'application_id': self.application_id,
        }
        self.user_details_record ={
            'email': 'knights@ni.com'
        }

    # def test_no_link_to_master_summay_page_without_completed_tasks(self):
    #     """
    #     Test to assert that the 'Childcare-Training-Guidance' page can be rendered.
    #     """
    #     with mock.patch('nanny_models.childcare_training.ChildcareTraining.api.get_record') as nanny_api_get, \
    #         mock.patch('nanny_models.childcare_training.ChildcareTraining.api.get_record') as identity_api_get:
    #
    #         for task in self.tasks:
    #             self.application_record[task] = 'NOT_STARTED'
    #
    #         nanny_api_get.return_value.record = self.application_record
    #
    #         response = self.client.get(reverse('Task-List') + '?id=' + self.application_id)
    #         link = reverse('Declaration-Summary') + '?id=' + self.application_id
    #
    #         self.assertNotIn(link, response.body)

    # def test_link_to_master_summary_page_when_completed_tasks(self):
    #     """
    #     Test to assert that the 'Declaration-Summary' page can be rendered if all the tasks are 'COMPLETED'.
    #     """
    #     with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
    #         mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
    #         nanny_api_read.side_effect = side_effect
    #         identity_api_read.side_effect = side_effect
    #
    #         for task in self.tasks:
    #             self.application_record[task] = 'COMPLETED'
    #
    #         response = self.client.get(reverse('Task-List') + '?id=' + 'a4e6633f-5339-4de5-ae03-69c71fd008b3')
    #
    #         self.assertContains(
    #             response,
    #             '<a href="{}">'.format(
    #                 reverse('declaration:Master-Summary') + '?id=' + 'a4e6633f-5339-4de5-ae03-69c71fd008b3'),
    #             html=True
    #         )

    def test_can_render_master_summary_page(self):
        """
        Test to assert that the 'Master-Summary' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            for task in self.tasks:
                self.application_record[task] = 'COMPLETED'

            response = self.client.get(reverse('declaration:Master-Summary') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.MasterSummary)

    def test_post_request_to_master_summary_redirects(self):
        """
        Test to assert that POST requests to the 'Master-Summary' page redirect to the 'Declaration-Guidance' page.
        """
        response = self.client.post(reverse('declaration:Master-Summary') + '?id=' + self.application_id)
        found = resolve(response.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(found.func.view_class, views.DeclarationGuidance)

    def test_declaration_guidance_page_can_be_rendered(self):
        """
        Test to assert that the 'Master-Summary' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('declaration:Declaration-Guidance') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.DeclarationGuidance)

    def test_final_declaration_page_can_be_reviewd(self):
        """
        Test to assert that the 'Final-Declaration' page can be rendered.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('declaration:Declaration-Summary') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.FinalDeclaration)

    def test_can_complete_final_declaration(self):
        """
        Test to assert that the Final Declaration form can be completed and a POST request redirects to the
        'Payment-Details' page.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.post(reverse('declaration:Declaration-Summary') + '?id=' + self.application_id,
                                        {
                                            'follow_rules': True,
                                            'share_info_declare': True,
                                            'information_correct_declare': True,
                                            'change_declare': True,
                                        })
            found = resolve(response.url)

            self.assertEqual(response.status_code, 302)
            # self.assertEqual(found.func.view_class, views.PaymentDetails)

    def test_unselected_declaration_boxes_raise_form_error(self):
        """
        Test that not selecting each declaration box raises the respective error.
        """
        pass
