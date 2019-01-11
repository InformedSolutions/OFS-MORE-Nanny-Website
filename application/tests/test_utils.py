import uuid

from django.http import HttpResponse


mock_nanny_application = {
    'application_status': 'DRAFTING',
    'application_reference': 'NA0000000001',
    'application_id': '998fd8ec-b96b-4a71-a1a1-a7a3ae186729',
    'date_submitted': '2018-07-31 17:20:46.011717+00',
    'date_updated': '2018-07-31 17:20:46.011717+00',
    'childcare_training_status': 'NOT_STARTED',
    'login_details_status': 'COMPLETED',
    'personal_details_status': 'NOT_STARTED',
    'dbs_status': 'NOT_STARTED',
    'address_to_be_provided': True,
    'login_details_arc_flagged': False,
    'personal_details_arc_flagged': False,
    'childcare_address_status': 'COMPLETED',
    'childcare_address_arc_flagged': False,
    'first_aid_status': 'COMPLETED',
    'first_aid_training_arc_flagged': False,
    'childcare_training_arc_flagged': False,
    'criminal_record_check_arc_flagged': False,
    'insurance_cover_status': 'COMPLETED',
    'insurance_cover_arc_flagged': False,
}

mock_personal_details_record = {
    'first_name': 'The Dark Lord',
    'middle_names': '',
    'last_name': 'Selenium',
    'date_of_birth': '2000-01-01',
    'lived_abroad': True,
    'your_children': False,
}

mock_childcare_training_record = {
    'level_2_training': False,
    'common_core_training': False,
    'no_training': False
}

mock_dbs_record = {
    'lived_abroad': 'False',
    'dbs_number': '000000000012',
    'convictions': 'False',
    'is_ofsted_dbs': 'True',
    'on_dbs_update_service': None
}

mock_home_address = {
    'street_line1': 'Test',
    'street_line2': None,
    'town': 'Middle Earth',
    'county': None,
    'postcode': 'WA14 4PA',
    'childcare_address': False,
}

mock_childcare_address_record = {
    'childcare_address_id': '7e6f1bf3-ee36-444d-99c6-b521d51a484f',
    'street_line1': 'Test',
    'street_line2': None,
    'town': 'New New York',
    'county': None,
    'postcode': 'WA14 4PA',
    'application_id': '998fd8ec-b96b-4a71-a1a1-a7a3ae186729',
}

mock_first_aid_record = {
    'training_organisation': 'St Johns Ambulance',
    'course_title': 'Pediatric First Aid',
    'course_date': '2016-03-31'
}

mock_insurance_cover_record = {
    'public_liability': True
}

mock_identity_record = {
    'email': 'test@informed.com',
    'application_id': 'a4e6633f-5339-4de5-ae03-69c71fd008b3',
    'magic_link_sms': '12345',
    'sms_resend_attempts': 0,
    'mobile_number': '000000000012',
    'magic_link_email': 'ABCDEFGHIJKL',
    'add_phone_number': '',
}

mock_payment_record = {
    'payment_id': 'a4e6633f-6339-4de5-ae03-69c71fd008b3',
    'application_id': 'a4e6633f-5339-4de5-ae03-69c71fd008b3',
    'payment_reference': 'NA0000000001',
    'payment_submitted': True,
    'payment_authorised': True
}

mock_declaration_record = {
    'follow_rules': True,
    'share_info_declare': True,
    'information_correct_declare': True,
    'confirm_declare': True,
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

dbs_check_response = HttpResponse()
dbs_check_response.status_code = 200
dbs_check_response.record = mock_dbs_record

first_aid_response = HttpResponse()
first_aid_response.status_code = 200
first_aid_response.record = mock_first_aid_record

insurance_cover_response = HttpResponse()
insurance_cover_response.status_code = 200
insurance_cover_response.record = mock_insurance_cover_record

childcare_address_response = HttpResponse()
childcare_address_response.status_code = 200
childcare_address_response.record = mock_childcare_address_record

declaration_response = HttpResponse()
declaration_response.status_code = 200
declaration_response.record = mock_declaration_record

payment_response = HttpResponse()
payment_response.status_code = 200
payment_response.record = mock_payment_record

identity_response = HttpResponse()
identity_response.status_code = 200
identity_response.record = mock_identity_record

arc_comments_response = HttpResponse()
arc_comments_response.status_code = 404


mock_endpoint_return_values = {
    'application': nanny_application_response,
    'applicant-personal-details': personal_details_response,
    'childcare-training': childcare_training_response,
    'childcare-address': childcare_address_response,
    'applicant-home-address': home_address_response,
    'dbs-check': dbs_check_response,
    'first-aid': first_aid_response,
    'insurance-cover': insurance_cover_response,
    'declaration': declaration_response,
    'user': identity_response,
    'arc-comments': arc_comments_response,
    'payment': payment_response
}


def side_effect(endpoint_name, *args, **kwargs):
    return mock_endpoint_return_values[endpoint_name]

def side_effect_childcare_address_list(endpoint_name, *args, **kwargs):
    list_response = childcare_address_response
    list_response.record['childcare_address_id'] = uuid.uuid4()
    list_response.record = [list_response.record]
    return list_response
