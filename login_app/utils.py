import random
import re
import string
import time

from urllib.parse import urlencode

from django import forms
from django.conf import settings
from django.shortcuts import reverse


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
