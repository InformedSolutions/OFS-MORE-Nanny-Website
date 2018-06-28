from ..tests import DBSTests, authenticate
from ...views import *
from django.urls import resolve
from django.template.response import TemplateResponse
from unittest import mock
from nanny_models.dbs_check import DbsCheck
import uuid

@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class DBSDetailEntryTests(DBSTests):

    def test_can_render_page_with_initial(self):
        """
        Test to assert that the 'dbs details' page can be rendered with an initial value.
        """

        with mock.patch('nanny_models.dbs_check.DbsCheck.api.get_record') as nanny_api_get:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = self.sample_dbs

            response = self.client.get(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_accept_correct_submission_without_convictions(self):
        """
        Test to assert that the 'dbs details' page can accept a valid entry for dbs details, and redirects to summary
        due to no convictions
        """

        with mock.patch('nanny_models.dbs_check.DbsCheck.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.dbs_check.DbsCheck.api.put'), \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get_app:
            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = self.sample_dbs

            response = self.client.post(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }), data=self.sample_dbs)

            self.assertEqual(response.status_code, 302)

    def test_can_accept_correct_submission_with_convictions(self):
        """
        Test to assert that the 'dbs details' page can accept a valid entry for dbs details, and redirects to post dbs
        page due to existing convictions
        """

        with mock.patch('nanny_models.dbs_check.DbsCheck.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.dbs_check.DbsCheck.api.put'), \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get_app:
            nanny_api_get_app.return_value.status_code = 200
            self.sample_dbs['convictions'] = 'True'
            nanny_api_get_app.return_value.record = self.sample_app
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = self.sample_dbs

            response = self.client.post(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }), data=self.sample_dbs)

            found = resolve(response.url)

            self.assertEqual(found.func.view_class, DBSUpload)

            self.assertEqual(response.status_code, 302)

    def test_can_reject_incorrect_submission_without_convictions(self):
        """
        Test to assert that the 'dbs details' page will deny an invalid form
        """

        with mock.patch('nanny_models.dbs_check.DbsCheck.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.dbs_check.DbsCheck.api.put'), \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_get_app:
            nanny_api_get_app.return_value.status_code = 200
            nanny_api_get_app.return_value.record = self.sample_app
            self.sample_dbs['dbs_number'] = 12
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = self.sample_dbs

            response = self.client.post(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }), data=self.sample_dbs)

            self.assertEqual(response.status_code, 200)