import uuid
from unittest import mock

from ..tests import DBSTests, authenticate
from ...views import *

from nanny.test_utils import side_effect


@mock.patch("nanny.db_gateways.IdentityGatewayActions.read", authenticate)
class DBSPostTests(DBSTests):

    def test_can_render_page_with_record(self):
        """
        Test to assert that the 'post certificate' page can be rendered correctly.
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
            mock.patch('nanny.db_gateways.NannyGatewayActions.put') as nanny_api_put:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('dbs:DBS-Upload', get={
                'id': uuid.UUID,
            }))

            self.assertEqual(response.status_code, 200)
