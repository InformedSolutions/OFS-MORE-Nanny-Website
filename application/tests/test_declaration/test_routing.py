from http.cookies import SimpleCookie
from unittest import mock

from django.http import HttpResponse
from django.test import modify_settings, TestCase
from django.urls import resolve, reverse

from application.presentation.utilities import NO_ADDITIONAL_CERTIFICATE_INFORMATION
from application.presentation.declaration import views
from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions
from application.tests.test_utils import side_effect, mock_endpoint_return_values, mock_dbs_record, \
    mock_nanny_application
from application.presentation.declaration.views import confirmation as confirmation_view


@modify_settings(MIDDLEWARE={
    'remove': [
        'middleware.CustomAuthenticationHandler',
    ]
})
class DeclarationRoutingTests(TestCase):

    def setUp(self):
        self.application_id = 'ef78049d-40fb-4808-943c-593fa3a9700b'
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})
        self.tasks = (
            'login_details_status',
            'personal_details_status',
            'childcare_address_status',
            'first_aid_status',
            'childcare_training_status',
            'dbs_status',
            'insurance_cover_status',
        )
        self.nanny_models = views.MasterSummary.model_names
        self.application_record = {
            'application_id': self.application_id,
        }
        self.user_details_record = {
            'email': 'knights@ni.com'
        }

    def test_no_link_to_master_summary_page_without_completed_tasks(self):
        """
        Test to assert that the 'Childcare-Training-Guidance' page can be rendered.
        """
        self.skipTest('testNotImplemented')

        # The below test is not functional.
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            for task in self.tasks:
                self.application_record[task] = 'NOT_STARTED'

            nanny_api_read.return_value.record = self.application_record

            response = self.client.get(reverse('Task-List') + '?id=' + self.application_id)
            link = reverse('Declaration-Summary') + '?id=' + self.application_id

            self.assertNotIn(link, response.body)

    def test_link_to_master_summary_page_when_completed_tasks(self):
        """
        Test to assert that the 'Declaration-Summary' page can be rendered if all the tasks are 'COMPLETED'.
        """
        self.skipTest('testNotImplemented')

        # The below test is not functional.
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            for task in self.tasks:
                self.application_record[task] = 'COMPLETED'

            response = self.client.get(reverse('Task-List') + '?id=' + 'a4e6633f-5339-4de5-ae03-69c71fd008b3')

            self.assertContains(
                response,
                '<a href="{}">'.format(
                    reverse('declaration:Master-Summary') + '?id=' + 'a4e6633f-5339-4de5-ae03-69c71fd008b3'),
                html=True
            )

    def test_can_render_master_summary_page(self):
        """
        Test to assert that the 'Master-Summary' page can be rendered.
        """

        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            for task in self.tasks:
                self.application_record[task] = 'COMPLETED'

            response = self.client.get(reverse('declaration:Master-Summary') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.MasterSummary)

    def test_can_render_master_summary_page_returned_application(self):
        """
                Test to assert that the 'Master-Summary' page can be rendered.
                """

        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            for task in self.tasks:
                self.application_record[task] = 'COMPLETED'

            self.application_record["application_status"] = "FURTHER_INFORMATION"
            #
            self.application_record["personal_details_arc_flagged"] = "False"
            self.application_record["childcare_address_arc_flagged"] = "False"
            self.application_record["first_aid_arc_flagged"] = "True"
            self.application_record["childcare_training_arc_flagged"] = "False"
            self.application_record["dbs_arc_flagged"] = "False"
            self.application_record["insurance_cover_arc_flagged"] = "False"

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
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.get(reverse('declaration:Declaration-Guidance') + '?id=' + self.application_id)
            found = resolve(response.request.get('PATH_INFO'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(found.func.view_class, views.DeclarationGuidance)

    def test_final_declaration_page_can_be_reviewed(self):
        """
        Test to assert that the 'Final-Declaration' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
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
        self.skipTest('testNotImplemented')

        # The below test is not functional.
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
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
        self.skipTest('testNotImplemented')

    def test_sends_survey_email_get_confirmation_page(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            # Set DBS Mock parameters
            updated_mock_nanny_application = mock_nanny_application

            updated_mock_nanny_application['application_status'] = 'DRAFTING'

            # Update side effect function
            updated_mock_nanny_application_response = HttpResponse()
            updated_mock_nanny_application_response.status_code = 200
            updated_mock_nanny_application_response.record = updated_mock_nanny_application

            updated_mock_endpoint_return_values = mock_endpoint_return_values
            updated_mock_endpoint_return_values['application'] = updated_mock_nanny_application_response

            nanny_api_read.side_effect = \
                lambda endpoint_name, *args, **kwargs: updated_mock_endpoint_return_values[endpoint_name]

            response = self.client.get(reverse('declaration:confirmation') + '?id=' + self.application_id)

            self.assertEqual(response.status_code, 200)
            send_email_mock.assert_called_with('test@informed.com', {'first_name': 'The Dark Lord', 'ref': 'NA000001'},
                                               'ca1acc2f-cfc7-4d20-b5d6-5bb17fce1d0a')

    def test_can_render_confirmation_page_capita_info_lived_abroad(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            # Set DBS Mock parameters
            updated_mock_dbs_record = mock_dbs_record

            updated_mock_dbs_record['is_ofsted_dbs'] = 'True'
            updated_mock_dbs_record['certificate_information'] = 'Some Info'
            updated_mock_dbs_record['lived_abroad'] = 'True'

            # Update side effect function
            updated_dbs_check_response = HttpResponse()
            updated_dbs_check_response.status_code = 200
            updated_dbs_check_response.record = updated_mock_dbs_record

            updated_mock_endpoint_return_values = mock_endpoint_return_values
            updated_mock_endpoint_return_values['dbs-check'] = updated_dbs_check_response

            nanny_api_read.side_effect = \
                lambda endpoint_name, *args, **kwargs: updated_mock_endpoint_return_values[endpoint_name]

            # Make get request
            response = self.client.get(reverse('declaration:confirmation') + '?id=' + self.application_id)

            # DBS and Lived Abroad
            self.assertContains(response, 'Post your DBS certificate')
            self.assertContains(response, 'Email your criminal record certificates from abroad')
            self.assertNotContains(response,
                                   "We'll review your application to make sure we have everything that we need.")

    def test_can_render_confirmation_page_capita_info_not_lived_abroad(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            # Set DBS Mock parameters
            updated_mock_dbs_record = mock_dbs_record

            updated_mock_dbs_record['is_ofsted_dbs'] = True
            updated_mock_dbs_record['certificate_information'] = 'Some Info'
            updated_mock_dbs_record['lived_abroad'] = False

            # Update side effect function
            updated_dbs_check_response = HttpResponse()
            updated_dbs_check_response.status_code = 200
            updated_dbs_check_response.record = updated_mock_dbs_record

            updated_mock_endpoint_return_values = mock_endpoint_return_values
            updated_mock_endpoint_return_values['dbs-check'] = updated_dbs_check_response

            nanny_api_read.side_effect = \
                lambda endpoint_name, *args, **kwargs: updated_mock_endpoint_return_values[endpoint_name]

            # Make get request
            response = self.client.get(reverse('declaration:confirmation') + '?id=' + self.application_id)

            # DBS Only
            self.assertContains(response, 'Send your documents')
            self.assertNotContains(response, 'Email your criminal record certificates from abroad')
            self.assertNotContains(response,
                                   "We'll review your application to make sure we have everything that we need.")

    def test_can_render_confirmation_page_capita_no_info_lived_abroad(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            # Set DBS Mock parameters
            updated_mock_dbs_record = mock_dbs_record

            updated_mock_dbs_record['is_ofsted_dbs'] = True
            updated_mock_dbs_record['certificate_information'] = NO_ADDITIONAL_CERTIFICATE_INFORMATION[0]
            updated_mock_dbs_record['lived_abroad'] = True

            # Update side effect function
            updated_dbs_check_response = HttpResponse()
            updated_dbs_check_response.status_code = 200
            updated_dbs_check_response.record = updated_mock_dbs_record

            updated_mock_endpoint_return_values = mock_endpoint_return_values
            updated_mock_endpoint_return_values['dbs-check'] = updated_dbs_check_response

            nanny_api_read.side_effect = \
                lambda endpoint_name, *args, **kwargs: updated_mock_endpoint_return_values[endpoint_name]

            # Make get request
            response = self.client.get(reverse('declaration:confirmation') + '?id=' + self.application_id)

            # Lived abroad Only
            self.assertNotContains(response, 'Post your DBS certificate')
            self.assertContains(response, 'Email your criminal record certificates from abroad')
            self.assertNotContains(response,
                                   "We'll review your application to make sure we have everything that we need.")

    def test_can_render_confirmation_page_capita_no_info_not_lived_abroad(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            # Set DBS Mock parameters
            updated_mock_dbs_record = mock_dbs_record

            updated_mock_dbs_record['is_ofsted_dbs'] = True
            updated_mock_dbs_record['certificate_information'] = NO_ADDITIONAL_CERTIFICATE_INFORMATION[0]
            updated_mock_dbs_record['lived_abroad'] = False

            # Update side effect function
            updated_dbs_check_response = HttpResponse()
            updated_dbs_check_response.status_code = 200
            updated_dbs_check_response.record = updated_mock_dbs_record

            updated_mock_endpoint_return_values = mock_endpoint_return_values
            updated_mock_endpoint_return_values['dbs-check'] = updated_dbs_check_response

            nanny_api_read.side_effect = \
                lambda endpoint_name, *args, **kwargs: updated_mock_endpoint_return_values[endpoint_name]

            # Make get request
            response = self.client.get(reverse('declaration:confirmation') + '?id=' + self.application_id)

            # No dbs No good conduct
            self.assertNotContains(response, 'Post your DBS certificate')
            self.assertNotContains(response, 'Email your criminal record certificates from abroad')
            self.assertContains(response,
                                   "We'll review your application to make sure we have everything that we need.")

    def test_can_render_confirmation_page_not_capita_lived_abroad(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            # Set DBS Mock parameters
            updated_mock_dbs_record = mock_dbs_record

            updated_mock_dbs_record['is_ofsted_dbs'] = False
            updated_mock_dbs_record['lived_abroad'] = True

            # Update side effect function
            updated_dbs_check_response = HttpResponse()
            updated_dbs_check_response.status_code = 200
            updated_dbs_check_response.record = updated_mock_dbs_record

            updated_mock_endpoint_return_values = mock_endpoint_return_values
            updated_mock_endpoint_return_values['dbs-check'] = updated_dbs_check_response

            nanny_api_read.side_effect = \
                lambda endpoint_name, *args, **kwargs: updated_mock_endpoint_return_values[endpoint_name]

            # Make get request
            response = self.client.get(reverse('declaration:confirmation') + '?id=' + self.application_id)

            # DBS and Lived abroad
            self.assertContains(response, 'Post your DBS certificate')
            self.assertContains(response, 'Email your criminal record certificates from abroad')
            self.assertNotContains(response,
                                   "We'll review your application to make sure we have everything that we need.")

    def test_can_render_confirmation_page_not_capita_not_lived_abroad(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read, \
                mock.patch.object(confirmation_view, 'send_email') as send_email_mock:
            nanny_api_put.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            # Set DBS Mock parameters
            updated_mock_dbs_record = mock_dbs_record

            updated_mock_dbs_record['is_ofsted_dbs'] = False
            updated_mock_dbs_record['certificate_information'] = NO_ADDITIONAL_CERTIFICATE_INFORMATION[0]
            updated_mock_dbs_record['lived_abroad'] = False

            # Update side effect function
            updated_dbs_check_response = HttpResponse()
            updated_dbs_check_response.status_code = 200
            updated_dbs_check_response.record = updated_mock_dbs_record

            updated_mock_endpoint_return_values = mock_endpoint_return_values
            updated_mock_endpoint_return_values['dbs-check'] = updated_dbs_check_response

            nanny_api_read.side_effect = \
                lambda endpoint_name, *args, **kwargs: updated_mock_endpoint_return_values[endpoint_name]

            # Make get request
            response = self.client.get(reverse('declaration:confirmation') + '?id=' + self.application_id)

            # DBS only
            self.assertContains(response, 'Send your documents')
            self.assertNotContains(response, 'Email your criminal record certificates from abroad')
            self.assertNotContains(response, "We'll review your application to make sure we have everything that we need.")
