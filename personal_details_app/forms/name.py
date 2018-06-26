from django import forms

import re


from djcelery.utils import now
from govuk_forms.forms import GOVUKForm


class PersonalDetailsNameForm(GOVUKForm):
    """
     GOV.UK form for the Personal Details: Name page
     """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    auto_replace_widgets = True

    first_name = forms.CharField(
        label='First name',
        error_messages={
            'required': 'Please enter your first name',
            'max_length': 'First name must be under 100 characters long'
        }
    )

    middle_names = forms.CharField(
        label='Middle names',
        required=False,
        error_messages={
            'max_length': 'Middles names must be under 100 characters long'
        }
    )

    last_name = forms.CharField(
        label='Last name',
        error_messages={
            'required': 'Please enter your last name',
            'max_length': 'Last name must be under 100 characters long'
        }
    )

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