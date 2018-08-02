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
    'last_name': 'Selenium',
}

mock_childcare_training_record = {
    'level_2_training': False,
    'common_core_training': False,
    'no_training': False
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

identity_response = HttpResponse()
identity_response.status_code = 200
identity_response.record = mock_identity_record


mock_endpoint_return_values = {
    'application': nanny_application_response,
    'applicant-personal-details': personal_details_response,
    'childcare-training': childcare_training_response,
    'user': identity_response,
}


def side_effect(endpoint_name, *args, **kwargs):
    return mock_endpoint_return_values[endpoint_name]

