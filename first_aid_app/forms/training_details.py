from django import forms

import re


from djcelery.utils import now
from govuk_forms.forms import GOVUKForm

from first_aid_app.widgets.customfields import CustomSplitDateField


class FirstAidTrainingDetailsForm(GOVUKForm):
    """
    GOV.UK form for the First aid training: details page
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    auto_replace_widgets = True

    first_aid_training_organisation = forms.CharField(
        label='Training organisation',
        max_length=50,
        error_messages={
            'required': 'Please enter the title of your course',
            'max_length': 'The name of the training organisation must be under 50 characters'
        }
    )

    title_of_training_course = forms.CharField(
        label='Title of training course',
        max_length=50,
        error_messages={
            'required': 'Please enter the title of the course',
            'max_length': 'The title of the course must be under 50 characters'
        }
    )

    course_date = CustomSplitDateField(
        label='Date you completed course',
        help_text='For example, 31 03 2016',
        error_messages={'required': 'Please enter the full date, including the day, month and year'},
        
    )
