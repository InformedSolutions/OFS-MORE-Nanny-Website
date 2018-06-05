from govuk_forms.forms import GOVUKForm

from django.forms import forms

from login_app.utils import DBSNumberField, PhoneNumberField


class BaseSecurityQuestionForm(GOVUKForm):
    """

    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem on this page'

    security_answer = None

    def clean_security_answer(self):
        security_answer = self.cleaned_data['security_answer']

        self.answer = ''  # TODO:

        if self.answer.replace(' ', '') != security_answer.replace(' ', ''):
            raise forms.ValidationError('Your answer must match what you told us in your application')

        return security_answer

    def __init__(self, *args, **kwargs):
        self.answer = None  # TODO: Insert API call to determine the correct answer.
        super(BaseSecurityQuestionForm, self).__init__(*args, **kwargs)


class DBSSecurityQuestionForm(BaseSecurityQuestionForm):

    security_answer = DBSNumberField(label='DBS Number', required=True, error_messages={'required': 'Please give an answer'})


class DoBSecurityQuestionForm(BaseSecurityQuestionForm):

    security_answer = None


class MobileNumberSecurityQuestionForm(BaseSecurityQuestionForm):

    security_answer = PhoneNumberField(label='Your mobile number', number_type='mobile', required=True, error_messages={'required': 'Please give an answer'})


