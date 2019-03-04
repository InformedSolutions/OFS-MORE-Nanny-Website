from django import forms

from application.presentation.utilities import NannyForm
from datetime import date
from application.presentation.customfields import CustomSplitDateField
from dateutil.relativedelta import relativedelta


class FirstAidTrainingDetailsForm(NannyForm):
    """
    GOV.UK form for the First aid training: details page
    """
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'

    training_organisation = forms.CharField(
        label='Training organisation',
        error_messages={
            'required': 'Please enter the name of the training organisation',
        }
    )

    course_title = forms.CharField(
        label='Title of training course',
        error_messages={
            'required': 'Please enter the title of the course',
        }
    )

    course_date = CustomSplitDateField(
        label='Date you completed course',
        help_text='For example, 31 03 2016',
        error_messages={'required': 'Please enter the full date, including the day, month and year'},
        
    )

    def clean_first_aid_training_organisation(self):
        organisation = self.cleaned_data['first_aid_training_organisation']
        if len(organisation) > 50:
            raise forms.ValidationError('The name of the training organisation must be under 50 characters')

        return organisation

    def clean_title_of_training_course(self):
        title = self.cleaned_data['title_of_training_course']
        if len(title) > 50:
            raise forms.ValidationError('The title of the course must be under 50 characters long')

        return title

    def clean_course_date(self):
        course_day = self.cleaned_data['course_date'].day
        course_month = self.cleaned_data['course_date'].month
        course_year = self.cleaned_data['course_date'].year
        course_date = date(course_year, course_month, course_day)
        today = date.today()
        date_difference = relativedelta(today, course_date)
        if date_difference.years >= 3:
            raise forms.ValidationError("You must have completed your first aid course in the last 3 years")

        return course_date




