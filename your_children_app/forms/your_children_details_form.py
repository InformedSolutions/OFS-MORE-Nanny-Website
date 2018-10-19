import re
from datetime import date

from nanny import NannyForm, CustomSplitDateFieldDOB
from django import forms
from django.conf import settings

from nanny.db_gateways import NannyGatewayActions


class YourChildrenDetailsForm(NannyForm):
    """
     GOV.UK form for the Personal Details: Name page
     """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = "There was a problem with your children's details"
    auto_replace_widgets = True

    first_name = forms.CharField(
        label='First name',
        error_messages={
            'required': "Please enter their first name",
            'max_length': 'First name must be under 100 characters long'
        }
    )
    middle_names = forms.CharField(
        label='Middle names (if you have any on your DBS check)',
        required=False,
        error_messages={
            'max_length': 'Middle names must be under 100 characters long'
        }
    )
    last_name = forms.CharField(
        label='Last name',
        error_messages={
            'required': 'Please enter their last name',
            'max_length': 'Last name must be under 100 characters long'
        }
    )
    date_of_birth = CustomSplitDateFieldDOB(
        label='Date of birth',
        help_text='For example, 31 03 1980',
        error_messages={
            'required': 'Please enter the full date, including the day, month and year'
        }
    )

    def __init__(self, *args, **kwargs):
        """
        Method to initialise the form for the entry of child details
        :param args: arguments passed to the form
        :param kwargs: arguments passed to the form as keyword, such as the application ID
        """
        if 'id' in kwargs['initial']:
            self.application_id_local = kwargs['initial']['id']
        elif 'data' in kwargs and 'id' in kwargs['data']:
            self.application_id_local = kwargs['data']['id']

        if 'child_id' in kwargs['initial']:
            self.childcare_address_id = kwargs['initial']['child_id']

        super(YourChildrenDetailsForm, self).__init__(*args, **kwargs)

        # TODO - Adapt the section below for this form, set all self.fields, consider the view file
        # attempt to mirror the functions present in childcare address entry views/forms
        # If information was previously entered, display it on the form

        # set all field vars to None
        # if child_id in self


        postcode = None
        if 'childcare_address_id' in self:
            response = NannyGatewayActions().list('childcare-address', params={'childcare_address_id': self.childcare_address_id})
            if response.status_code == 200:
                postcode = response.record[0]['postcode']
            self.pk = self.childcare_address_id

        self.fields['postcode'].initial = postcode
        self.field_list = ['postcode']


    def clean_first_name(self):
        """
        First name validation
        :return: string
        """
        first_name = self.cleaned_data['first_name']
        if len(first_name) > 100:
            raise forms.ValidationError("First name must be under 100 characters long")
        return first_name

    def clean_middle_names(self):
        """
        Last name validation
        :return: string
        """
        middle_names = self.cleaned_data['middle_names']
        if len(middle_names) > 100:
            raise forms.ValidationError("Middle names must be under 100 characters long")
        return middle_names

    def clean_last_name(self):
        """
        Last name validation
        :return: string
        """
        last_name = self.cleaned_data['last_name']
        if len(last_name) > 100:
            raise forms.ValidationError("Last name must be under 100 characters long")
        return last_name

    def clean_date_of_birth(self):
        """
        Date of birth validation (calculate if age is more than 16)
        :return: birth day, birth month, birth year
        """
        birth_day = self.cleaned_data['date_of_birth'].day
        birth_month = self.cleaned_data['date_of_birth'].month
        birth_year = self.cleaned_data['date_of_birth'].year
        applicant_dob = date(birth_year, birth_month, birth_day)
        today = date.today()
        age = today.year - applicant_dob.year - ((today.month, today.day) < (applicant_dob.month, applicant_dob.day))
        if age < 16:
            raise forms.ValidationError('Please only use this page for children aged under 16')
        date_today_diff = today.year - applicant_dob.year - (
                (today.month, today.day) < (applicant_dob.month, applicant_dob.day))
        if len(str(birth_year)) < 4:
            raise forms.ValidationError('Please enter the whole year (4 digits)')
        if date_today_diff < 0:
            raise forms.ValidationError('Please check the year')

        return self.cleaned_data['date_of_birth']
