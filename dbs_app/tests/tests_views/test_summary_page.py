from unittest import mock
import uuid

from ..tests import DBSTests, authenticate
from ...views import *

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class DBSSummaryTests(DBSTests):

    def test_can_render_page_with_record(self):
        """
        Test to assert that the 'dbs summary' page can be rendered with a dbs record supplied.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('dbs:Summary', get={
                'id': uuid.UUID,
            }))

            self.assertEqual(response.status_code, 200)

    def test_post_request_updates_status(self):
        """
        Test to assert that the update tasks to complete method is called, and a redirect is successfully issued upon
        a post request
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('dbs:Summary'), data={
                'id': self.sample_app['application_id'],
                'dbs_number': '123',
            })

            # Checks that the api has attempted to change the criminal record check status to done and then redirects
            self.assertTrue(nanny_api_put.called)
            self.assertEqual(response.status_code, 302)
