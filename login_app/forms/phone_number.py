from govuk_forms.forms import GOVUKForm

from login_app.utils import PhoneNumberField


class PhoneNumbersForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem with your phone number'

    mobile_number = PhoneNumberField(number_type='mobile',
                                     label='Your mobile number',
                                     required=True,
                                     error_messages={'required': "Please enter a mobile number"})

    other_phone_number = PhoneNumberField(number_type='other_phone',
                                          label='Other phone number (optional)',
                                          required=False)
