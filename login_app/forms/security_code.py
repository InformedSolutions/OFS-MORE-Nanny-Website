from django import forms

from govuk_forms.forms import GOVUKForm


class SecurityCodeForm(GOVUKForm):
    """
    GOV.UK form for entering a security code.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'

    sms_code = forms.IntegerField(label='Security code', required=True,
                                  error_messages={'required': 'Please enter the 5 digit code we sent to your mobile'})

    def clean_sms_code(self):
        """
        Method to validate the SMS code entered by the user.
        :return: sms_code: string giving the cleaned sms code.
        """
        sms_code = str(self.cleaned_data['sms_code'])

        if len(sms_code) < 5:
            raise forms.ValidationError('The code must be 5 digits. You have entered fewer than 5 digits')
        if len(sms_code) > 5:
            raise forms.ValidationError('The code must be 5 digits. You have entered more than 5 digits')
        if sms_code != self.correct_sms_code:
            raise forms.ValidationError('Invalid code. Check the code we sent to your mobile.')
        return sms_code

    def __init__(self, *args, **kwargs):
        self.correct_sms_code = kwargs.pop('correct_sms_code')
        super(SecurityCodeForm, self).__init__(*args, **kwargs)
