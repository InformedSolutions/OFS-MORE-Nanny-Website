from django import forms

import re

from djcelery.utils import now
from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import NumberInput, InlineRadioSelect


class DBSDetailsForm(GOVUKForm):
    """
    GOV.UK form for the DBS Details Page
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'

    # Overrides standard NumberInput widget too give wider field
    widget_instance = NumberInput()
    widget_instance.input_classes = 'form-control form-control-1-4'

    convictions_choices = (
        (True, 'Yes'), (False, 'No')
    )

    dbs_number = forms.IntegerField(
        label='DBS certificate number',
        help_text='12-digit number on your certificate',
        error_messages={
            'required': 'Please enter your DBS certificate number',
        },
        widget=widget_instance,
    )

    convictions = forms.ChoiceField(
        label='Do you have any criminal cautions or convictions?',
        help_text='Include any information recorded on your certificate',
        choices=convictions_choices,
        error_messages={
            'required': 'Please say if you have any criminal cautions or convictions',
        },
        widget=InlineRadioSelect
    )

    def clean_dbs_number(self):
        """
        DBS certificate number validation
        :return: integer
        """
        # is_valid() call strips leading 0 required by DBS number. Use raw str input from user instead of cleaned_data.
        dbs_number = self.data['dbs_number']
        if len(str(dbs_number)) != 12:
            raise forms.ValidationError('Check your certificate: the number should be 12 digits long')

        return dbs_number
