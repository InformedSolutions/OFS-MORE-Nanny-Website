from django import forms

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import Widget

from login_app.utils import DBSNumberField, PhoneNumberField


class NannyFormInput(forms.widgets.TextInput, Widget):
    input_classes = "nanny-form form-control"


class BaseSecurityQuestionForm(GOVUKForm):
    """
    Base GOV.UK form from which individual security question forms will inherit.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'

    security_answer = None

    def clean_security_answer(self):
        security_answer = self.cleaned_data['security_answer']

        if self.correct_answer.replace(' ', '') != security_answer.replace(' ', ''):
            raise forms.ValidationError('Your answer must match what you told us in your application')

        return security_answer


class DBSSecurityQuestionForm(BaseSecurityQuestionForm):

    security_answer = DBSNumberField(label='DBS Number', required=True,
                                     error_messages={'required': 'Please give an answer'},
                                     widget=NannyFormInput)
    help_text = 'Please enter your DBS certificate number.'


class DoBSecurityQuestionForm(BaseSecurityQuestionForm):

    security_answer = None
    help_text = None


class MobileNumberSecurityQuestionForm(BaseSecurityQuestionForm):

    security_answer = PhoneNumberField(label='Your mobile number',
                                       number_type='mobile',
                                       required=True,
                                       error_messages={'required': 'Please give an answer'},
                                       widget=NannyFormInput)
    help_text = 'Please enter your mobile number.'

