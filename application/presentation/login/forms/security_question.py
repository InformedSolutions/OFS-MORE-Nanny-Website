from django import forms

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import Widget, TextInput

from application.presentation.utilities import DBSNumberField, PhoneNumberField
from application.presentation.customfields import CustomSplitDateFieldDOB


class NannyFormInput(TextInput, Widget):
    input_classes = "nanny-form form-control"


class DBSSecurityQuestionForm(GOVUKForm):
    """
    GOV.UK form for the dbs number security question.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'
    help_text = 'Please enter your DBS certificate number.'
    correct_answer = {}

    dbs_number = DBSNumberField(label='DBS Number', required=True,
                                error_messages={'required': 'Please give an answer'},
                                widget=NannyFormInput)

    def clean_dbs_number(self):
        dbs_number = str(self.cleaned_data['dbs_number'])

        if self.correct_answer['dbs_number'].replace(' ', '') != dbs_number.replace(' ', ''):
            raise forms.ValidationError('Your answer must match what you told us in your application')

        return dbs_number


class PersonalDetailsSecurityQuestionForm(GOVUKForm):
    """
    GOV.UK form for the personal details security question.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'
    help_text = 'Please enter your postcode and date of birth'
    correct_answer = {}

    date_of_birth = CustomSplitDateFieldDOB(label='Date of birth',
                                            help_text='For example, 31 03 1980',
                                            error_messages={'required': 'Please give an answer'})

    postcode = forms.CharField(label='Postcode',
                               required=True,
                               error_messages={'required': 'Please give an answer'},
                               widget=NannyFormInput)

    def clean_date_of_birth(self):
        date_of_birth = str(self.cleaned_data['date_of_birth'])

        if self.correct_answer['date_of_birth'].replace(' ', '') != date_of_birth.replace(' ', ''):
            raise forms.ValidationError('Your answer must match what you told us in your application')

        return date_of_birth

    def clean_postcode(self):
        postcode = str(self.cleaned_data['postcode'])

        if self.correct_answer['postcode'].replace(' ', '') != postcode.replace(' ', ''):
            raise forms.ValidationError('Your answer must match what you told us in your application')

        return postcode


class MobileNumberSecurityQuestionForm(GOVUKForm):
    """
    GOV.UK form for the mobile phone security question.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'
    help_text = 'Please enter your mobile number.'
    correct_answer = {}

    mobile_number = PhoneNumberField(label='Your mobile number',
                                     number_type='mobile',
                                     required=True,
                                     error_messages={'required': 'Please give an answer'},
                                     widget=NannyFormInput)

    def clean_mobile_number(self):
        mobile_number = str(self.cleaned_data['mobile_number'])

        if self.correct_answer['mobile_number'].replace(' ', '') != mobile_number.replace(' ', ''):
            raise forms.ValidationError('Your answer must match what you told us in your application')

        return mobile_number
