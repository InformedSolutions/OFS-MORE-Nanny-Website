import json
import random
import re
import requests
import string
import time

from urllib.parse import urlencode

from django import forms
from django.conf import settings
from django.shortcuts import reverse


def test_notify():
    # If running exclusively as a test return true to avoid overuse of the notify API
    if settings.EXECUTING_AS_TEST:
        return True

    if test_notify_connection():
        return True
    else:
        return False


def test_notify_settings():
    """
    Function to check if url for notify app is defined.
    return; Bool
    """
    url = settings.NOTIFY_URL
    if 'url' in locals():
        return True
    else:
        return False


def test_notify_connection():
    """
    Function to test connection with Notify API.
    :return: Bool
    """
    try:
        # Test Sending Email
        header = {'content-type': 'application/json'}
        req = requests.Session()
        notification_request = {
            'email': 'simulate-delivered@notifications.service.gov.uk',
            'personalisation': {
                'link': 'test'
            },
            'templateId': 'ecd2a788-257b-4bb9-8784-5aed82bcbb92'
        }
        r = req.post(settings.NOTIFY_URL + '/api/v1/notifications/email/',
                     json.dumps(notification_request),
                     headers=header, timeout=10)
        if r.status_code == 201:
            return True
    except Exception as ex:
        print(ex)
        return False


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url


def generate_email_validation_link(email_address):
    link = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(12)]).upper()
    full_link = str(settings.PUBLIC_APPLICATION_URL) + '/validate/' + link  # + '?email_address=' + email_address

    return full_link, int(time.time())


def generate_sms_code():
    return ''.join([random.choice(string.digits[1:]) for n in range(5)]), int(time.time())


class PhoneNumberField(forms.CharField):

    def __init__(self, number_type=None, *args, **kwargs):
        if number_type not in ('mobile', 'other_phone'):
            raise ValueError("You must pass number_type as either 'mobile' or 'other_phone'.")

        self.number_type = number_type
        self.regex_type = 'MOBILE' if 'mobile' in self.number_type else 'PHONE'

        super(PhoneNumberField, self).__init__(*args, **kwargs)

    def clean(self, number):
        """
        Clean method for the PhoneNumberField.
        :param number: Number entered by user to be validated.
        :return: number: Cleaned number input.
        """
        if not self.required and number == '':  # Skip the regex match if unrequired field left blank.
            return number

        no_space_number = number.replace(' ', '')

        if not len(no_space_number):
            raise forms.ValidationError('Please enter a {} number'.format(self.regex_type.lower()))

        if re.match(settings.REGEX[self.regex_type], no_space_number) is None:
            raise forms.ValidationError('Please enter a valid {} number'.format(self.regex_type.lower()))

        return number


class DBSNumberField(forms.CharField):

    def clean(self, dbs_number):
        """
        :param dbs_number:
        :return:
        """
        # if not len(dbs_number):
        #     raise forms.ValidationError('')

        if len(dbs_number) > 12:
            raise forms.ValidationError('The certificate number should be 12 digits long')
        if len(dbs_number) < 12:
            raise forms.ValidationError('The certificate number should be 12 digits long')
        return dbs_number
