from unittest import mock

from django.test import TestCase

from nanny.test_utils import side_effect, mock_nanny_application, mock_personal_details_record, mock_identity_record, \
    mock_childcare_training_record, mock_childcare_address_record, mock_dbs_record, mock_home_address, mock_first_aid_record, \
    mock_insurance_cover_record, mock_declaration_record

from ..views import payment


class PaymentTests(TestCase):
    """
    Tests for asserting payment functionality
    """

    app_id = None

    def setUp(self):
        self.user_details_record = mock_identity_record
        self.nanny_application_record = mock_nanny_application
        self.app_id = self.nanny_application_record['application_id']
        self.personal_details_record = mock_personal_details_record
        self.childcare_training_record = mock_childcare_training_record
        self.dbs_record = mock_dbs_record
        self.home_address_record = mock_home_address
        self.childcare_address_record = mock_childcare_address_record
        self.first_aid_record = mock_first_aid_record
        self.insurance_cover_record = mock_insurance_cover_record
        self.identity_record = mock_identity_record
        self.declaration_record = mock_declaration_record

    def test_can_create_an_export(self):
        """
        Test can generate a JSON representation of an application
        """
        with mock.patch('nanny.db_gateways.NannyGatewayActions.read') as nanny_api_read, \
                mock.patch('nanny.db_gateways.NannyGatewayActions.list') as nanny_api_list, \
                mock.patch('nanny.db_gateways.IdentityGatewayActions.read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect
            nanny_api_list.side_effect = side_effect

            response = payment.create_full_application_export(self.app_id)
            self.assertIsNotNone(response)
