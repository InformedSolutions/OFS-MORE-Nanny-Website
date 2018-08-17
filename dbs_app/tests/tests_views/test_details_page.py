from unittest import mock
import uuid

from django.urls import resolve

from ..tests import DBSTests, authenticate
from dbs_app import views
from dbs_app.views import build_url

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class DBSDetailEntryTests(DBSTests):

    def test_can_render_page_with_initial(self):
        """
        Test to assert that the 'dbs details' page can be rendered with an initial value.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_accept_correct_submission_without_convictions(self):
        """
        Test to assert that the 'dbs details' page can accept a valid entry for dbs details, and redirects to summary
        due to no convictions
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }), data=self.sample_dbs)

            self.assertEqual(response.status_code, 302)

    def test_can_accept_correct_submission_with_convictions(self):
        """
        Test to assert that the 'dbs details' page can accept a valid entry for dbs details, and redirects to post dbs
        page due to existing convictions
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            test_record = self.sample_dbs
            test_record['convictions'] = True

            response = self.client.post(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }), data=test_record)

            # As this response can redirect to multiple places, the view which is rendered on redirect is checked below
            found = resolve(response.url)
            self.assertEqual(found.func.view_class, views.DBSUpload)
            self.assertEqual(response.status_code, 302)

    def test_can_reject_incorrect_submission_without_convictions(self):
        """
        Test to assert that the 'dbs details' page will deny an invalid form
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            self.sample_dbs['dbs_number'] = 12

            response = self.client.post(build_url('dbs:Details', get={
                'id': uuid.UUID,
            }), data=self.sample_dbs)

            self.assertEqual(response.status_code, 200)
