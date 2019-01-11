from datetime import date

from django import forms

from application.presentation.utilities import NannyForm
from application.presentation.customfields import CustomSplitDateFieldDOB


class PersonalDetailsDOBForm(NannyForm):
    """
    GOV.UK form for the Your personal details: date of birth page
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    date_of_birth = CustomSplitDateFieldDOB(label='Date of birth', help_text='For example, 31 03 1980', error_messages={
        'required': 'Please enter the full date, including the day, month and year'})

    def clean_date_of_birth(self):
        """
        Date of birth validation (calculate if age is less than 18)
        :return: birth day, birth month, birth year
        """
        birth_day = self.cleaned_data['date_of_birth'].day
        birth_month = self.cleaned_data['date_of_birth'].month
        birth_year = self.cleaned_data['date_of_birth'].year
        applicant_dob = date(birth_year, birth_month, birth_day)
        today = date.today()
        age = today.year - applicant_dob.year - ((today.month, today.day) < (applicant_dob.month, applicant_dob.day))
        if age < 18:
            raise forms.ValidationError('You must be 18 or older to be a nanny')
        date_today_diff = today.year - applicant_dob.year - (
                (today.month, today.day) < (applicant_dob.month, applicant_dob.day))
        if len(str(birth_year)) < 4:
            raise forms.ValidationError('Please enter the whole year (4 digits)')
        if date_today_diff < 0:
            raise forms.ValidationError('Please check the year')

        return self.cleaned_data['date_of_birth']