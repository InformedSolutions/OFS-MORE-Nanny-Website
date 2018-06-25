from unittest import mock

from django.core.urlresolvers import reverse
from django.http import SimpleCookie
from django.test import TestCase
from django.urls import resolve

class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id):
    record = {
            'application_id': application_id,
            'email': 'test@informed.com'
        }
    return CustomResponse(record)


@mock.patch("identity_models.user_details.UserDetails.api.get_record", authenticate)
class FirstAidTrainingTests(TestCase):

    app_id = '3575d19f-5bfc-4fcc-a7cf-229323876043'


    def setUp(self):
        self.client.cookies = SimpleCookie({'_ofs': 'test@informed.com'})

    def test_can_access_guidance(self):
        r = self.client.get(reverse('first-aid:First-Aid-Guidance'), {'id': self.app_id})
        self.assertEqual(r.status_code, 200)

    def test_can_access_details(self):
        r = self.client.get(reverse('first-aid:Training-Details'), {'id': self.app_id})
        self.assertEqual(r.status_code, 200)

    def test_can_access_declaration(self):
        r = self.client.get(reverse('first-aid:First-Aid-Declaration'), {'id': self.app_id})
        self.assertEqual(r.status_code, 200)

    def test_can_access_summary(self):
        with mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_app_get, \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_app_put:
            nanny_api_app_get.return_value.status_code = 200
            nanny_api_app_get.return_value.record = {
                'application_id': '3575d19f-5bfc-4fcc-a7cf-229323876043',
                'first_aid_training_status': 'IN_PROGRESS'
            }
            nanny_api_app_put.return_value.status_code = 201

            r = self.client.get(reverse('first-aid:First-Aid-Summary'), {'id': self.app_id})
            p = self.client.post(reverse('first-aid:First-Aid-Summary'), {'id': self.app_id})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(p.status_code, 302)

    def test_can_submit_details_form(self):
        with mock.patch('nanny_models.first_aid.FirstAidTraining.api.get_record') as nanny_api_get, \
                mock.patch('nanny_models.first_aid.FirstAidTraining.api.create') as nanny_api_post, \
                mock.patch('nanny_models.first_aid.FirstAidTraining.api.put') as nanny_api_put, \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.get_record') as nanny_api_app_get, \
                mock.patch('nanny_models.nanny_application.NannyApplication.api.put') as nanny_api_app_put:
            nanny_api_get.return_value.status_code = 200
            nanny_api_get.return_value.record = {
                'training_organisation': 'St Johns Ambulance',
                'course_title': 'Pediatric First Aid',
                'course_date': '2016-03-31'
            }
            nanny_api_post.return_value.status_code = 201
            nanny_api_put.return_value.status_code = 201
            nanny_api_app_get.return_value.status_code = 200
            nanny_api_app_get.return_value.record = {
                'application_id': '3575d19f-5bfc-4fcc-a7cf-229323876043',
                'first_aid_training_status': 'IN_PROGRESS'
            }
            nanny_api_app_put.return_value.status_code = 201

            data = {
                'id': self.app_id,
                'first_aid_training_organisation': 'St Johns Ambulance',
                'title_of_training_course': 'Pediatric First Aid',
                'course_date_0': '12',
                'course_date_1': '3',
                'course_date_2': '2017',
            }

            r = self.client.post(reverse('first-aid:Training-Details'), data, params={'id': self.app_id})
            self.assertEqual(r.status_code, 302)

    def test_invalid_course_date_stopped(self):

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
