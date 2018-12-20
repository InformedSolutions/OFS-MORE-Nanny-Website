import re

from django import forms
from django.conf import settings
from govuk_forms.forms import GOVUKForm

from nanny.db_gateways import NannyGatewayActions


class ChildcareAddressForm(GOVUKForm):
    """
    GOV.UK form for childcare address postcode search
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode', error_messages={'required': 'Please enter your postcode'})

    def __init__(self, *args, **kwargs):
        """
        Method to configure the initialisation of the childcare address postcode search
        :param args: arguments passed to the form
        :param kwargs: keyword arguments passed to the form, e.g. application ID
        """

        # extract the application id from the 'initial' or 'data' dictionaries.
        if 'id' in kwargs['initial']:
            self.application_id_local = kwargs['initial']['id']
        elif 'data' in kwargs and 'id' in kwargs['data']:
            self.application_id_local = kwargs['data']['id']

        # extract the childcare address id from the 'initial' dictionary.
        if 'childcare_address_id' in kwargs['initial']:
            self.childcare_address_id = kwargs['initial']['childcare_address_id']

        super(ChildcareAddressForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        postcode = None
        if 'childcare_address_id' in self:
            response = NannyGatewayActions().list('childcare-address', params={'childcare_address_id': self.childcare_address_id})
            if response.status_code == 200:
                postcode = response.record[0]['postcode']
            self.pk = self.childcare_address_id

        self.fields['postcode'].initial = postcode
        self.field_list = ['postcode']

    def clean_postcode(self):
        """
        Postcode validation
        :return: string
        """
        postcode = self.cleaned_data['postcode']
        postcode_no_space = postcode.replace(" ", "")
        postcode_uppercase = postcode_no_space.upper()
        if re.match(settings.REGEX['POSTCODE_UPPERCASE'], postcode_uppercase) is None:
            raise forms.ValidationError('Please enter a valid postcode')
        return postcode


class ChildcareAddressManualForm(GOVUKForm):
    """
    GOV.UK form for the childcare address page for manual entry
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    street_line1 = forms.CharField(label='Address line 1', error_messages={
        'required': 'Please enter the first line of your address'})
    street_line2 = forms.CharField(label='Address line 2', required=False)
    town = forms.CharField(label='Town or city',
                           error_messages={'required': 'Please enter the name of the town or city'})
    county = forms.CharField(label='County (optional)', required=False)
    postcode = forms.CharField(label='Postcode', error_messages={'required': 'Please enter your postcode'})

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

        super(ChildcareAddressManualForm, self).__init__(*args, **kwargs)

        if hasattr(self, 'childcare_address_id'):
            response = NannyGatewayActions().list('childcare-address', params={'childcare_address_id': self.childcare_address_id})
            if response.status_code == 200:
                record = response.record[0]
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
        street_line1 = self.cleaned_data['street_line1']
        if len(street_line1) > 50:
            raise forms.ValidationError('The first line of your address must be under 50 characters long')
        return street_line1

    def clean_street_line2(self):
        """
        Street name and number line 2 validation
        :return: string
        """
        street_line2 = self.cleaned_data['street_line2']
        if len(street_line2) > 50:
            raise forms.ValidationError('The second line of your address must be under 50 characters long')
        return street_line2

    def clean_town(self):
        """
        Town validation
        :return: string
        """
        town = self.cleaned_data['town']
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
        county = self.cleaned_data['county']
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
        postcode = self.cleaned_data['postcode']
        postcode_no_space = postcode.replace(" ", "")
        postcode_uppercase = postcode_no_space.upper()
        if re.match(settings.REGEX['POSTCODE_UPPERCASE'], postcode_uppercase) is None:
            raise forms.ValidationError('Please enter a valid postcode')
        return postcode


class ChildcareAddressLookupForm(GOVUKForm):
    """
    GOV.UK form for the childcare address page for postcode search results
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    address = forms.ChoiceField(label='Select address', required=True,
                                error_messages={'required': 'Please select your address'})

    def __init__(self, *args, **kwargs):
        """
        Method to configure the initialisation of the Your personal details: home address form for postcode search
        :param args: arguments passed to the form
        :param kwargs: keyword arguments passed to the form, e.g. application ID
        """
        # extract the application id from the 'initial' or 'data' dictionaries.
        if 'id' in kwargs['initial']:
            self.application_id_local = kwargs['initial']['id']
        elif 'data' in kwargs and 'id' in kwargs['data']:
            self.application_id_local = kwargs['data']['id']

        # extract the childcare address id from the 'initial' dictionaries.
        try:
            self.childcare_address_id = kwargs.pop('childcare_address_id')
        except KeyError:
            self.childcare_address_id = None

        super(ChildcareAddressLookupForm, self).__init__(*args, **kwargs)

        if 'choices' in kwargs['initial']:
            self.choices = kwargs['initial']['choices']
            self.fields['address'].choices = self.choices

    def clean_address(self):
        return int(self.cleaned_data['address'])