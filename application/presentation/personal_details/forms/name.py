from django import forms
from django.utils.html import escape
from django.conf import settings

from govuk_forms.widgets import RadioSelect

from application.presentation.utilities import NannyForm


def get_title_options():
    """
    Get the options for the title radio button form
    :return: tuples of choices
    """
    options = ()
    for title in settings.TITLE_OPTIONS:
        options += ((title, title),)
    options += (('Other', 'Other'),)
    return options


class PersonalDetailsNameForm(NannyForm):
    """
     GOV.UK form for the Personal Details: Name page
     """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True
    reveal_conditionally = {'title': {'Other': 'other_title'}}

    title = forms.ChoiceField(
        label='Title',
        choices=get_title_options(),
        required=True,
        widget=RadioSelect,
        error_messages={
            'required': 'Please select a title'
        }
    )

    other_title = forms.CharField(
        label='Other',
        required=False,
        error_messages={
            'required': 'Please enter a title'
        }
    )

    first_name = forms.CharField(
        label='First name',
        error_messages={
            'required': 'Please enter your first name',
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
            'required': 'Please enter your last name',
            'max_length': 'Last name must be under 100 characters long'
        }
    )

    def clean_other_title(self):
        """
        Other title validation
        :return: string
        """
        other_title = self.cleaned_data['other_title']
        if self.cleaned_data.get('title') == 'Other':
            if len(other_title) == 0:
                raise forms.ValidationError('Please tell us your title')
            if len(other_title) > 100:
                raise forms.ValidationError('Titles must be under 100 characters long')
        return other_title

    def clean_first_name(self):
        """
        First name validation
        :return: string
        """
        first_name = escape(self.cleaned_data['first_name'])
        if len(first_name) > 100:
            raise forms.ValidationError("First name must be under 100 characters long")
        return first_name

    def clean_middle_names(self):
        """
        Last name validation
        :return: string
        """
        middle_names = escape(self.cleaned_data['middle_names'])
        if len(middle_names) > 100:
            raise forms.ValidationError("Middle names must be under 100 characters long")
        return middle_names

    def clean_last_name(self):
        """
        Last name validation
        :return: string
        """
        last_name = escape(self.cleaned_data['last_name'])
        if len(last_name) > 100:
            raise forms.ValidationError("Last name must be under 100 characters long")
        return last_name
