import requests
import json
from datetime import datetime, timedelta

from django.conf import settings
from application.services.db_gateways import NannyGatewayActions

DBS_API_ENDPOINT = settings.DBS_URL


def read_dbs(dbs_certificate_number):
    params = {'certificate_number': dbs_certificate_number}
    response = requests.get(DBS_API_ENDPOINT + '/api/v1/dbs/' + dbs_certificate_number + '/', data=params, verify=False)
    if response.status_code == 200:
        response.record = json.loads(response.text)
    return response


def dbs_date_of_birth_no_match(record, application_id):
    """
    :param application: the application to be tested against
    :param record: the record from the dbs api
    :return: a boolean to represent if there is no match between the applicant dob and the dbs dob
    """
    if record is None:
        return False

    app_details = NannyGatewayActions().read('applicant-personal-details', {'application_id':application_id})
    return not _dbs_dob_matches(record, app_details.record['date_of_birth'])


def _dbs_dob_matches(record, applicant_date_of_birth):
    return datetime.strptime(applicant_date_of_birth, '%Y-%m-%d') == datetime.strptime(record['date_of_birth'], '%Y-%m-%d')


def dbs_within_three_months(record):
    """
    :param record: the issue date of the dbs
    :return: a boolean to represent if there the dbs was issued within three months of today
    """
    date_of_issue = datetime.strptime(record['date_of_issue'], '%Y-%m-%d')
    now = datetime.today()
    if now - timedelta(3 * 365 / 12) <= date_of_issue:
        return True
    else:
        return False