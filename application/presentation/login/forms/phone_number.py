from govuk_forms.widgets import Widget
from application.presentation.utilities import *


class NannyFormInput(forms.widgets.NumberInput, Widget):
    input_classes = "nanny-form form-control"


class PhoneNumbersForm(GOVUKForm):
    """
    GOV.UK form for entering contact phone numbers.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'

    mobile_number = PhoneNumberField(number_type='mobile',
                                     label='Your mobile number',
                                     required=True,
                                     error_messages={'required': "Please enter a mobile number"},
                                     widget=NannyFormInput)

    other_phone_number = PhoneNumberField(number_type='other_phone',
                                          label='Other phone number (optional)',
                                          required=False,
                                          widget=NannyFormInput)
