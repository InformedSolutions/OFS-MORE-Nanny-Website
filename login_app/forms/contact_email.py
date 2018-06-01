from django import forms

import re

from govuk_forms.forms import GOVUKForm
from login_app import utils


class ContactEmailForm(GOVUKForm):
    """
    GOV.UK form for entering an email address.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem on this page'
    auto_replace_widgets = True

    email_address = forms.EmailField(required=True, error_messages={'required': "Please enter an email address"})

    def clean_email_address(self):
        """
        Method for email address validation.
        :return: email_address; cleaned email_address as a string.
        """
        email_address = self.cleaned_data['email_address']
        # RegEx for valid e-mail addresses
        if re.match(utils.REGEX['EMAIL'], email_address) is None:
            raise forms.ValidationError('Please enter a valid email address, like yourname@example.com')
        return email_address