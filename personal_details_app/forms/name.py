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
        max_length=100,
        error_messages={
            'required': 'Please enter your first name',
            'max_length': 'First name must be under 100 characters long'
        }
    )

    middle_names = forms.CharField(
        label='Middles names',
        max_length=100,
        error_messages={
            'max_length': 'Middles names must be under 100 characters long'
        }
    )

    last_name = forms.CharField(
        label='Last name',
        max_length=100,
        error_messages={
            'required': 'Please enter your last name',
            'max_length': 'Last name must be under 100 characters long'
        }
    )
