from django.http import HttpResponse


mock_nanny_application = {
    'application_status': 'SUBMITTED',
    'application_id': '998fd8ec-b96b-4a71-a1a1-a7a3ae186729',
    'date_submitted': '2018-07-31 17:20:46.011717+00',
    'date_updated': '2018-07-31 17:20:46.011717+00',
    'childcare_training_status': 'NOT_STARTED',
}

mock_personal_details_record = {
    'first_name': 'The Dark Lord',
    'middle_names': '',
    'last_name': 'Selenium',
    'date_of_birth': '2000-01-01',
    'lived_abroad': True
}

mock_childcare_training_record = {
    'level_2_training': False,
    'common_core_training': False,
    'no_training': False
}

mock_home_address = {
    'street_line1': 'Test',
    'street_line2': None,
    'town': 'Test Town',
    'county': None,
    'postcode': 'WA14 4PA'
}

mock_identity_record = {
    'email': 'test@informed.com'
}


nanny_application_response = HttpResponse()
nanny_application_response.status_code = 200
nanny_application_response.record = mock_nanny_application

personal_details_response = HttpResponse()
personal_details_response.status_code = 200
personal_details_response.record = mock_personal_details_record

childcare_training_response = HttpResponse()
childcare_training_response.status_code = 200
childcare_training_response.record = mock_childcare_training_record

home_address_response = HttpResponse()
home_address_response.status_code = 200
home_address_response.record = mock_home_address

identity_response = HttpResponse()
identity_response.status_code = 200
identity_response.record = mock_identity_record


mock_endpoint_return_values = {
    'application': nanny_application_response,
    'applicant-personal-details': personal_details_response,
    'childcare-training': childcare_training_response,
    'applicant-home-address': home_address_response,
    'user': identity_response,
}


def side_effect(endpoint_name, *args, **kwargs):
    return mock_endpoint_return_values[endpoint_name]

