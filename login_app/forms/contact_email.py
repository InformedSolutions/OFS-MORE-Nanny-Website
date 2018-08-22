from django import forms
from django.conf import settings

import re

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import Widget


class NannyFormInput(forms.widgets.EmailInput, Widget):
    input_classes = "nanny-form form-control"


class ContactEmailForm(GOVUKForm):
    """
    GOV.UK form for entering an email address.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    email_address = forms.EmailField(required=True,
                                     help_text='Make sure only you can access it',
                                     error_messages={'required': "Please enter an email address"},
                                     widget=NannyFormInput)

    def clean_email_address(self):
        """
        Method for email address validation.
        :return: email_address; cleaned email_address as a string.
        """
        email_address = self.cleaned_data['email_address']
        # RegEx for valid e-mail addresses
        if re.match(settings.REGEX['EMAIL'], email_address) is None:
            raise forms.ValidationError('Please enter a valid email address, like yourname@example.com')
        return email_address

    def __init__(self, *args, **kwargs):
        super(ContactEmailForm, self).__init__(*args, **kwargs)

        # Remove full stop from error message, if required. N.B. full-stop-stripper won't work here.
        if len(self.errors):
            if self.errors['email_address'].data[0].message == 'Enter a valid email address.':
                self.errors['email_address'].data[0].message = 'Please enter a valid email address, like yourname@example.com'
