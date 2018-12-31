from unittest import mock

from django.core.urlresolvers import reverse
from django.http import SimpleCookie
from django.test import TestCase

from application.services.db_gateways import NannyGatewayActions, IdentityGatewayActions
from application.tests.test_utils import side_effect, mock_identity_record


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id, *args, **kwargs):
    record = mock_identity_record
    return CustomResponse(record)


@mock.patch.object(IdentityGatewayActions, "read", authenticate)
class FirstAidTrainingTests(TestCase):
    app_id = '3575d19f-5bfc-4fcc-a7cf-229323876043'

    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})

    def test_can_access_guidance(self):
        r = self.client.get(reverse('first-aid:First-Aid-Guidance'), {'id': self.app_id})
        self.assertEqual(r.status_code, 200)

    def test_can_access_details(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            r = self.client.get(reverse('first-aid:Training-Details'), {'id': self.app_id})
            self.assertEqual(r.status_code, 200)

    def test_can_access_declaration(self):
        r = self.client.get(reverse('first-aid:First-Aid-Declaration'), {'id': self.app_id})
        self.assertEqual(r.status_code, 200)

    def test_can_access_summary(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            r = self.client.get(reverse('first-aid:First-Aid-Summary'), {'id': self.app_id})
            p = self.client.post(reverse('first-aid:First-Aid-Summary'), {'id': self.app_id})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(p.status_code, 302)

    def test_can_submit_details_form(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'patch') as nanny_api_patch, \
                mock.patch.object(NannyGatewayActions, 'create') as nanny_api_create, \
                mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect
            nanny_api_patch.side_effect = side_effect
            nanny_api_create.side_effect = side_effect

            data = {
                'id': self.app_id,
                'first_aid_training_organisation': 'St Johns Ambulance',
                'title_of_training_course': 'Pediatric First Aid',
                'course_date_0': '12',
                'course_date_1': '3',
                'course_date_2': '2017',
            }

            r = self.client.post(reverse('first-aid:Training-Details'), data, params={'id': self.app_id})
            self.assertEqual(r.status_code, 200)

    def test_invalid_course_date_stopped(self):
        with mock.patch.object(NannyGatewayActions, 'read') as nanny_api_read, \
                mock.patch.object(NannyGatewayActions, 'put') as nanny_api_put, \
                mock.patch.object(NannyGatewayActions, 'list'):
            nanny_api_read.side_effect = side_effect
            nanny_api_put.side_effect = side_effect

            data = {
                'id': self.app_id,
                'first_aid_training_organisation': 'St Johns Ambulance',
                'title_of_training_course': 'Pediatric First Aid',
                'course_date_0': '12',
                'course_date_1': '3',
                'course_date_2': '2014',
            }

            r = self.client.post(reverse('first-aid:Training-Details'), data, params={'id': self.app_id})
            self.assertEqual(r.status_code, 200)
