import re

from django import forms
from django.conf import settings
from django.utils.html import escape
import datetime

from application.services.db_gateways import NannyGatewayActions
from application.presentation.utilities import NannyForm
from application.presentation import form_fields


class HomeAddressForm(NannyForm):
    """
    GOV.UK form for childcare address postcode search
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode', error_messages={'required': 'Please enter your postcode'})

    def __init__(self, *args, **kwargs):
        """
        Method to configure the initialisation of the home address postcode search
        :param args: arguments passed to the form
        :param kwargs: keyword arguments passed to the form, e.g. application ID
        """

        super(HomeAddressForm, self).__init__(*args, **kwargs)
        self.field_list = ['postcode']

    def clean_postcode(self):
        """
        Postcode validation
        :return: string
        """
        postcode = escape(self.cleaned_data['postcode'])
        postcode_no_space = postcode.replace(" ", "")
        postcode_uppercase = postcode_no_space.upper()
        if re.match(settings.REGEX['POSTCODE_UPPERCASE'], postcode_uppercase) is None:
            raise forms.ValidationError('Please enter a valid postcode')
        return postcode


class HomeAddressManualForm(NannyForm):
    """
    GOV.UK form for the Your personal details: home address page for manual entry
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    ERROR_MESSAGE_DATE_BLANK = 'Enter the full date, including the day, month and year'
    ERROR_MESSAGE_DAY_OUT_OF_RANGE = 'Day must be between 1 and 31'
    ERROR_MESSAGE_MONTH_OUT_OF_RANGE = 'Month must be between 1 and 12'
    ERROR_MESSAGE_MOVED_IN_YEAR_BEFORE_1900 = 'Date moved in must be after 1900'
    ERROR_MESSAGE_YEAR_LESS_THAN_4_DIGITS = 'Enter the whole year (4 digits)'
    ERROR_MESSAGE_INVALID_DATE = 'Enter a real date'
    ERROR_MESSAGE_NON_NUMERIC = 'Use numbers for the date'

    ERROR_MESSAGE_MOVED_IN_DATE_AFTER_CURRENT_DATE = 'Date moved in must be today or in the past'
    ERROR_MESSAGE_MOVED_IN_DATE_AFTER_MOVED_OUT_DATE = 'Date you moved in must be before date you moved out'

    street_line1 = forms.CharField(label='Address line 1', error_messages={
        'required': 'Please enter the first line of your address'})
    street_line2 = forms.CharField(label='Address line 2', required=False)
    town = forms.CharField(label='Town or city',
                           error_messages={'required': 'Please enter the name of the town or city'})
    county = forms.CharField(label='County (optional)', required=False)
    postcode = forms.CharField(label='Postcode', error_messages={'required': 'Please enter your postcode'})

    moved_in_date = form_fields.CustomSplitDateFieldAddress(
        label='Moved in',
        required=True,
        help_text='For example, 31 3 1980',
        error_messages={'required': ERROR_MESSAGE_DATE_BLANK,
                        'incomplete': ERROR_MESSAGE_DATE_BLANK,
                        'max_today': ERROR_MESSAGE_MOVED_IN_DATE_AFTER_CURRENT_DATE,
                        'invalid': ERROR_MESSAGE_INVALID_DATE},
    )

    def __init__(self, *args, **kwargs):
        """
        Method to configure the initialisation of the manual entry form for childcare addresses
        :param args: arguments passed to the form
        :param kwargs: keyword arguments passed to the form, e.g. application ID
        """
        if 'id' in kwargs['initial']:
            self.application_id_local = kwargs['initial']['id']
        elif 'data' in kwargs and 'id' in kwargs['data']:
            self.application_id_local = kwargs['data']['id']

        if 'childcare_address_id' in kwargs['initial']:
            self.childcare_address_id = kwargs['initial']['childcare_address_id']

        super(HomeAddressManualForm, self).__init__(*args, **kwargs)

        if hasattr(self, 'childcare_address_id'):
            response = NannyGatewayActions().read('childcare-address', params={'childcare_address_id': self.childcare_address_id})
            if response.status_code == 200:
                record = response.record
                self.fields['street_line1'].initial = record['street_line1']
                self.fields['street_line2'].initial = record['street_line2']
                self.fields['town'].initial = record['town']
                self.fields['county'].initial = record['county']
                self.fields['postcode'].initial = record['postcode']
                self.pk = self.childcare_address_id
                self.field_list = ['street_line1', 'street_line2', 'town', 'county', 'postcode']

    def clean_street_line1(self):
        """
        Street name and number validation
        :return: string
        """
        street_line1 = escape(self.cleaned_data['street_line1'])
        if len(street_line1) > 50:
            raise forms.ValidationError('The first line of your address must be under 50 characters long')
        return street_line1

    def clean_street_line2(self):
        """
        Street name and number line 2 validation
        :return: string
        """
        street_line2 = escape(self.cleaned_data['street_line2'])
        if len(street_line2) > 50:
            raise forms.ValidationError('The second line of your address must be under 50 characters long')
        return street_line2

    def clean_town(self):
        """
        Town validation
        :return: string
        """
        town = escape(self.cleaned_data['town'])
        if re.match(settings.REGEX['TOWN'], town) is None:
            raise forms.ValidationError('Please spell out the name of the town or city using letters')
        if len(town) > 50:
            raise forms.ValidationError('The name of the town or city must be under 50 characters long')
        return town

    def clean_county(self):
        """
        County validation
        :return: string
        """
        county = escape(self.cleaned_data['county'])
        if county != '':
            if re.match(settings.REGEX['COUNTY'], county) is None:
                raise forms.ValidationError('Please spell out the name of the county using letters')
            if len(county) > 50:
                raise forms.ValidationError('The name of the county must be under 50 characters long')
        return county

    def clean_postcode(self):
        """
        Postcode validation
        :return: string
        """
        postcode = escape(self.cleaned_data['postcode'])
        postcode_no_space = postcode.replace(" ", "")
        postcode_uppercase = postcode_no_space.upper()
        if re.match(settings.REGEX['POSTCODE_UPPERCASE'], postcode_uppercase) is None:
            raise forms.ValidationError('Please enter a valid postcode')
        return postcode

    def clean_moved_in_date(self):
        moved_in_date = self.cleaned_data['moved_in_date']
        # get applicant's date of birth
        applicant_response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': self.application_id_local})
        # check that the moved in date is on or after the dob
        if applicant_response.status_code == 200:
            applicant_dob = datetime.datetime.strptime(applicant_response.record['date_of_birth'], '%Y-%m-%d').date()
            if moved_in_date < applicant_dob:
                raise forms.ValidationError('Please enter a move in date which is after your date of birth')




class HomeAddressLookupForm(NannyForm):
    """
    GOV.UK form for the childcare address page for postcode search results
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    ERROR_MESSAGE_DATE_BLANK = 'Enter the full date, including the day, month and year'
    ERROR_MESSAGE_DAY_OUT_OF_RANGE = 'Day must be between 1 and 31'
    ERROR_MESSAGE_MONTH_OUT_OF_RANGE = 'Month must be between 1 and 12'
    ERROR_MESSAGE_MOVED_IN_YEAR_BEFORE_1900 = 'Date moved in must be after 1900'
    ERROR_MESSAGE_YEAR_LESS_THAN_4_DIGITS = 'Enter the whole year (4 digits)'
    ERROR_MESSAGE_INVALID_DATE = 'Enter a real date'
    ERROR_MESSAGE_NON_NUMERIC = 'Use numbers for the date'

    ERROR_MESSAGE_MOVED_IN_DATE_AFTER_CURRENT_DATE = 'Date moved in must be today or in the past'
    ERROR_MESSAGE_MOVED_IN_DATE_AFTER_MOVED_OUT_DATE = 'Date you moved in must be before date you moved out'

    home_address = forms.ChoiceField(label='Select address', required=True,
                                     error_messages={'required': 'Please select your address'})

    moved_in_date = form_fields.CustomSplitDateFieldAddress(
        label='Moved in',
        required=True,
        help_text='For example, 31 3 1980',
        error_messages={'required': ERROR_MESSAGE_DATE_BLANK,
                        'incomplete': ERROR_MESSAGE_DATE_BLANK,
                        'max_today': ERROR_MESSAGE_MOVED_IN_DATE_AFTER_CURRENT_DATE,
                        'invalid': ERROR_MESSAGE_INVALID_DATE},
    )

    def __init__(self, *args, **kwargs):
        """
        Method to configure the initialisation of the Your personal details: home address form for postcode search
        :param args: arguments passed to the form
        :param kwargs: keyword arguments passed to the form, e.g. application ID
        """
        if 'id' in kwargs['initial']:
            self.application_id_local = kwargs['initial']['id']
        elif 'data' in kwargs and 'id' in kwargs['data']:
            self.application_id_local = kwargs['data']['id']

        super(HomeAddressLookupForm, self).__init__(*args, **kwargs)

        if 'choices' in kwargs['initial']:
            self.choices = kwargs['initial']['choices']
            self.fields['home_address'].choices = self.choices

    def clean_home_address(self):
        return int(self.cleaned_data['home_address'])

    def clean_moved_in_date(self):
        moved_in_date = self.cleaned_data['moved_in_date']
        # get applicant's date of birth
        applicant_response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': self.application_id_local})
        if applicant_response.status_code == 200:
            applicant_dob = datetime.datetime.strptime(applicant_response.record['date_of_birth'], '%Y-%m-%d').date()
            # check that the date is not before the dob
            if moved_in_date < applicant_dob:
                raise forms.ValidationError('Please enter a move in date which is after your date of birth')


