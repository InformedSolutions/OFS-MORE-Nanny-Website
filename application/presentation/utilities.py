"""
Generic helper functions
"""
import json
import random
import re
import string
import time
from urllib.parse import urlencode

import requests
from django import forms
from django.conf import settings
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from govuk_forms.forms import GOVUKForm

from application.services.db_gateways import NannyGatewayActions


class NeverCacheMixin(object):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(NeverCacheMixin, self).dispatch(*args, **kwargs)


class NannyForm(GOVUKForm):
    """
    Parent class from which all others will late inherit. Contains logic for checking the existence of ARC comments on
    fields.
    """

    def get_pk(self, pk):
        if pk:
            return pk
        else:
            return ''

    def get_endpoint(self, endpoint):
        if endpoint:
            return endpoint
        else:
            return ''

    def check_flags(self, application_id, endpoint=None, pk=None):
        """
        For a class to call this method it must set self.pk - this is the primary key of the entry against which the
        ArcComments table is being filtered.
        This method simply checks whether or not a field is flagged, raising a validation error if it is.
        """
        for field in self.fields:
            arc_comments_filter = NannyGatewayActions().list('arc-comments', params={'application_id': application_id,
                                                                                     'field_name': field,
                                                                                     'endpoint_name': self.get_endpoint(
                                                                                         endpoint),
                                                                                     'table_pk': self.get_pk(pk)})
            if arc_comments_filter.status_code == 200 and bool(arc_comments_filter.record[0]['flagged']):
                comment = arc_comments_filter.record[0]['comment']
                self.cleaned_data = ''
                self.add_error(field, forms.ValidationError(comment))
            # If fields cannot be flagged individually, check for flags using the bespoke methods.
            else:
                self.if_name(application_id, field, True, pk)
                self.if_home_address(application_id, field, True, endpoint, pk)

    def remove_flags(self, application_id, endpoint=None, pk=None):
        for field in self.fields:
            arc_comments_filter = NannyGatewayActions().list('arc-comments', params={'application_id': application_id,
                                                                                     'field_name': field,
                                                                                     'endpoint_name': self.get_endpoint(
                                                                                         endpoint),
                                                                                     'table_pk': self.get_pk(pk)})
            if arc_comments_filter.status_code == 200 and bool(arc_comments_filter.record[0]['flagged']):
                arc_record = arc_comments_filter.record[0]
                arc_record['flagged'] = False
                NannyGatewayActions().put('arc-comments', params=arc_record)
            # If fields cannot be flagged individually, check for flags using the bespoke methods.
            else:
                self.if_name(application_id, field, False, pk)
                self.if_home_address(application_id, field, False, endpoint, pk)

    def if_name(self, application_id, field, enabled, pk=None):
        """
        This checks if a name has been flagged, as first, middle or last cannot be flagged individually.
        It will be called on every field during the call to check_flags and remove_flags.
        :param field: The name of the field with which to query the database.
        :param enabled: Specify if you are setting the 'flagged' column to True or False.
        :return: None
        """
        if field in ('first_name', 'middle_names', 'last_name'):
            query_params = {'application_id': application_id, 'field_name': 'name', 'table_pk': self.get_pk(pk)}
            arc_comments_filter = NannyGatewayActions().list('arc-comments', params=query_params)
            if arc_comments_filter.status_code == 200 and bool(arc_comments_filter.record[0]['flagged']):
                if enabled and field == 'first_name':
                    comment = arc_comments_filter.record[0]['comment']
                    self.cleaned_data = ''
                    self.add_error(field, forms.ValidationError(comment))
                elif enabled and field != 'first_name':
                    self.add_error(field, forms.ValidationError(''))
                else:
                    arc_record = arc_comments_filter.record[0]
                    arc_record['flagged'] = False
                    NannyGatewayActions().put('arc-comments', params=arc_record)

    def if_home_address(self, application_id, field, enabled, endpoint=None, pk=None):
        """
        This checks if an address has been flagged, as constituent fields cannot be flagged individually.
        It will be called on every field during the call to check_flags and remove_flags.
        :param field: The name of the field with which to query the database.
        :param enabled: Specify if you are setting the 'flagged' column to True or False.
        :return: None
        """
        if endpoint == 'your-children':
            arc_comments_filter = NannyGatewayActions().list('arc-comments', params={
                'application_id': application_id,
                'endpoint_name': self.get_endpoint(endpoint),
                'field_name': 'address',
                'table_pk': self.get_pk(pk),
            })
            self.mtn_address_handler(arc_comments_filter, field, enabled)

        elif endpoint == 'childcare-address':
            arc_comments_filter = NannyGatewayActions().list('arc-comments', params={
                'application_id': application_id,
                'endpoint_name': self.get_endpoint(endpoint),
                'field_name': 'childcare_address',
            })
            self.mtn_address_handler(arc_comments_filter, field, enabled)

        elif endpoint == 'applicant-home-address':
            arc_comments_filter = NannyGatewayActions().list('arc-comments', params={
                'application_id': application_id,
                'endpoint_name': self.get_endpoint(endpoint),
                'field_name': 'home_address'
            })
            self.mtn_address_handler(arc_comments_filter, field, enabled)

        else:
            pass

    def mtn_address_handler(self, arc_comments_filter, field, enabled):
        if arc_comments_filter.status_code == 200 and bool(arc_comments_filter.record[0]['flagged']):
            if enabled and field == 'street_line1':
                comment = arc_comments_filter.record[0]['comment']
                self.cleaned_data = ''
                self.add_error(field, forms.ValidationError(comment))
            elif enabled and field != 'street_line1':
                self.cleaned_data = ''
                self.add_error(field, forms.ValidationError(''))
            else:
                arc_record = arc_comments_filter.record[0]
                arc_record['flagged'] = False
                NannyGatewayActions().put('arc-comments', params=arc_record)


def show_django_debug_toolbar(request):
    """
    Custom callback function to determine whether the django debug toolbar should be shown
    :param request: inbound HTTP request
    :return: boolean indicator used to trigger visibility of debug toolbar
    """
    return settings.DEBUG


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url


def app_id_finder(request):
    app_id = None
    if request.GET.get('id'):
        app_id = request.GET.get('id')
    if request.POST.get('id'):
        app_id = request.POST.get('id')

    return (app_id)


# TEST UTILTIIES #


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


def test_notify():
    # If running exclusively as a test return true to avoid overuse of the notify API
    if settings.EXECUTING_AS_TEST == 'True':
        return True

    return True
    #
    # if test_notify_connection():
    #     return True
    # else:
    #     return False


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
            'service_name': 'Nannies',
            'email': 'simulate-delivered@notifications.service.gov.uk',
            'personalisation': {
                'link': 'test'
            },
            'templateId': '45c6b63e-1973-45e5-99d7-25f2877bebd9'
        }
        r = req.post(settings.NOTIFY_URL + '/api/v1/notifications/email/',
                     json.dumps(notification_request),
                     headers=header, timeout=10)
        # both potentially legitimate status codes, depending on which api key is being used
        if r.status_code == 201 or r.status_code == 400:
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

        if len(no_space_number) != 11:
            raise forms.ValidationError('Please enter a valid {} number'.format(self.regex_type.lower()))

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


def app_id_finder(request):
    if request.GET.get('id'):
        app_id = request.GET.get('id')
    if request.POST.get('id'):
        app_id = request.POST.get('id')
    return (app_id)
