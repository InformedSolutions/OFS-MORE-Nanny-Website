from application.services.dbs import dbs_date_of_birth_no_match, dbs_within_three_months
from django.test import Client, modify_settings, SimpleTestCase, TestCase
import uuid
from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions
from unittest import mock

class CriminalRecordChecksTestHelper(SimpleTestCase):
    record = {'dbs_certificate_number': 123456789101, 'certificate_information': '', 'date_of_birth': '1994-11-23',
              'date_of_issue': '2017-02-01'}

    def test_dbs_date_of_birth_no_match_helper_true(self):
        applicant_record = {'date_of_birth': '1979-01-01'}
        result = dbs_date_of_birth_no_match(self.record, applicant_record)
        self.assertTrue(result)

    def test_dbs_date_of_birth_no_match_helper_false(self):
        applicant_record = {'date_of_birth': '1994-11-23'}
        result = dbs_date_of_birth_no_match(self.record, applicant_record)
        self.assertTrue(not result)

    def test_dbs_within_three_months_false(self):
        result = dbs_within_three_months(self.record)
        self.assertTrue(not result)