from ..tests import DBSTests, authenticate
from ...views import *
from django.urls import resolve
from django.template.response import TemplateResponse
from unittest import mock
from nanny_models.dbs_check import DbsCheck
import uuid

@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class DBSPostTests(DBSTests):

    def test_can_render_page_with_record(self):
        """
        Test to assert that the 'dbs details' page can be rendered with an initial value.
        """

        with mock.patch('nanny_models.dbs_check.DbsCheck.api.get_record') as nanny_api_get:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = self.sample_dbs

            response = self.client.get(build_url('dbs:DBS-Upload', get={
                'id': uuid.UUID,
            }))

            self.assertEqual(response.status_code, 200)
