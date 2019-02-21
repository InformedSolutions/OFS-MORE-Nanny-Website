import uuid
from unittest import mock

from django.template.response import TemplateResponse
from django.urls import resolve

from application.presentation.personal_details.views import *
from application.services.db_gateways import IdentityGatewayActions, NannyGatewayActions
from application.tests.test_utils import side_effect
from .test_utils import PersonalDetailsTests, authenticate


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class AddressSummaryTests(PersonalDetailsTests):

    def test_address_summary_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Address-Summary'))
        self.assertEqual(found.func.__name__, PersonalDetailSummaryAddressView.__name__)

    def test_can_render_address_summary_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get_addr:
            nanny_api_get_addr.side_effect = side_effect
            response = self.client.get(build_url('personal-details:Personal-Details-Address-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_post_address_summary_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_get_addr:
            nanny_api_get_addr.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Address-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/lived-abroad/' in response.url)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class CertificateTests(PersonalDetailsTests):

    def test_conduct_certificates_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Certificates-Of-Good-Conduct'))
        self.assertEqual(found.func.__name__, PersonalDetailCertificateView.__name__)

    def test_can_render_conduct_certificates_page(self):
        """
        Test to assert that the 'good conduct certificates' page can be rendered.
        """
        response = self.client.get(build_url('personal-details:Personal-Details-Certificates-Of-Good-Conduct', get={
            'id': uuid.UUID
        }))

        self.assertEqual(response.status_code, 200)

    def test_post_certificates_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Post-Certificates'))
        self.assertEqual(found.func.__name__, PersonalDetailsPostCertificateView.__name__)

    def test_can_render_post_certificates_page(self):
        """
        Test to assert that the 'good conduct certificates' page can be rendered.
        """
        response = self.client.get(build_url('personal-details:Personal-Details-Post-Certificates', get={
            'id': uuid.UUID
        }))

        self.assertEqual(response.status_code, 200)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class DateOfBirthTests(PersonalDetailsTests):

    def test_dob_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Date-Of-Birth'))
        self.assertEqual(found.func.__name__, PersonalDetailDOBView.__name__)

    def test_can_render_dob_page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_dob__page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.uuid4()
            }), {
                                            'date_of_birth_0': '23',
                                            'date_of_birth_1': '08',
                                            'date_of_birth_2': '1997'
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/your-home-address/' in response.url)

    def test_can_submit_invalid_dob_page(self):
        """
        Test to assert that the 'dob' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            identity_api_read.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Date-Of-Birth', get={
                'id': uuid.UUID
            }), {
                                            'date_of_birth_0': '',
                                            'date_of_birth_1': '',
                                            'date_of_birth_2': ''
                                        })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class LivedAbroadTests(PersonalDetailsTests):

    def test_lived_abroad_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Lived-Abroad'))
        self.assertEqual(found.func.__name__, PersonalDetailLivedAbroadView.__name__)

    def test_can_render_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_true_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be submitted.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }), {
                                            'lived_abroad': True
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/good-conduct-certificates/' in response.url)

    def test_can_submit_false_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be submitted.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }), {
                                            'lived_abroad': False
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/your-children/' in response.url)

    def test_can_submit_invalid_lived_abroad_page(self):
        """
        Test to assert that the 'lived abroad' page can be submitted.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch:
            nanny_api_read.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Lived-Abroad', get={
                'id': uuid.UUID
            }), {
                                            'lived_abroad': ''
                                        })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class ManualEntryTests(PersonalDetailsTests):

    def test_manual_entry_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Manual-Address'))
        self.assertEqual(found.func.__name__, PersonalDetailManualAddressView.__name__)

    def test_can_render_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_update_address_valid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                                            'street_line1': 'Test',
                                            'street_line2': '',
                                            'town': 'test',
                                            'county': '',
                                            'postcode': 'WA14 4PA'
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/home-address-details/' in response.url)

    def test_can_create_address_valid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                                            'street_line1': 'Test',
                                            'street_line2': '',
                                            'town': 'test',
                                            'county': '',
                                            'postcode': 'WA14 4PA'
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/home-address-details/' in response.url)

    def test_can_submit_invalid_manual_entry_page(self):
        """
        Test to assert that the 'manual entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Manual-Address', get={
                'id': uuid.UUID
            }), {
                                            'street_line1': '',
                                            'street_line2': '',
                                            'town': '',
                                            'county': '',
                                            'postcode': ''
                                        })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class NameTests(PersonalDetailsTests):

    def test_name_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Name'))
        self.assertEqual(found.func.__name__, PersonalDetailNameView.__name__)

    def test_can_render_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_valid_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.uuid4()
            }), {
                                            'first_name': 'Test',
                                            'last_name': 'Test'
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/your-date-of-birth/' in response.url)

    def test_can_submit_invalid_name_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Name', get={
                'id': uuid.UUID
            }), {
                                            'first_name': '',
                                            'last_name': ''
                                        })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class PostcodeEntryTests(PersonalDetailsTests):

    def test_postcode_entry_url_resolves_to_page(self):
        """
        Test to assert that the 'postcode entry' page can be resolved.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

        found = resolve(reverse('personal-details:Personal-Details-Home-Address'))

        self.assertEqual(found.func.__name__, PersonalDetailHomeAddressView.__name__)

    def test_can_render_postcode_entry_page(self):
        """
        Test to assert that the 'postcode entry' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.uuid4()
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_update_address_valid_postcode_entry_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.UUID
            }), {
                                            'postcode': 'WA14 4PA'
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/select-home-address/' in response.url)

    def test_can_create_address_valid_postcode_entry_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.UUID
            }), {
                                            'postcode': 'WA14 4PA'
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/select-home-address/' in response.url)

    def test_can_submit_invalid_postcode_entry_page(self):
        """
        Test to assert that the 'name' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Home-Address', get={
                'id': uuid.UUID
            }), {
                                            'postcode': ''
                                        })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class SelectAddressTests(PersonalDetailsTests):

    def test_select_address_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Select-Address'))
        self.assertEqual(found.func.__name__, PersonalDetailSelectAddressView.__name__)

    def test_can_render_select_address_page(self):
        """
        Test to assert that the 'select address' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Select-Address', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_update_address_valid_select_address_page(self):
        """
        Test to assert that the 'select address' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Select-Address', get={
                'id': uuid.UUID
            }), {
                                            'address': 1
                                        })

            self.assertEqual(response.status_code, 200)

    def test_can_submit_invalid_select_address_page(self):
        """
        Test to assert that the 'select address' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Select-Address', get={
                'id': uuid.UUID
            }), {'postcode': ''})

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class SummaryTests(PersonalDetailsTests):

    def test_summary_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Summary'))
        self.assertEqual(found.func.__name__, Summary.__name__)

    def test_can_render_summary_page(self):
        """
        Test to assert that the 'summary' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.get(build_url('personal-details:Personal-Details-Summary', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)


class YourChildrenTests(PersonalDetailsTests):

    def test_your_children_url_resolves_to_page(self):
        found = resolve(reverse('personal-details:Personal-Details-Your-Children'))
        self.assertEqual(found.func.__name__, PersonalDetailsYourChildrenView.__name__)

    def test_can_render_your_children_page(self):
        """
        Test to assert that the 'your children' page can be rendered.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            response = self.client.get(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }))

            self.assertEqual(response.status_code, 200)

    def test_can_submit_true_your_children_page(self):
        """
        Test to assert that the 'your children' page can be submitted.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }), {
                                            'your_children': True
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/check-answers/' in response.url)

    def test_can_submit_your_children_page(self):
        """
        Test to assert that the 'your children' page can be submitted.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }), {
                                            'your_children': False
                                        })

            self.assertEqual(response.status_code, 302)
            self.assertTrue('/check-answers/' in response.url)

    def test_can_submit_invalid_your_children_page(self):
        """
        Test to assert that the 'your children' page can be submitted.
        """
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'list') as nanny_api_list, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'delete') as nanny_api_delete, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(IdentityGatewayActions, 'read') as identity_api_read:
            nanny_api_read.side_effect = side_effect

            response = self.client.post(build_url('personal-details:Personal-Details-Your-Children', get={
                'id': uuid.UUID
            }), {
                                            'lived_abroad': ''
                                        })

            self.assertEqual(response.status_code, 200)
            self.assertTrue(type(response) == TemplateResponse)
