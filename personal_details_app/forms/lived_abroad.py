from django import forms

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import InlineRadioSelect


class PersonalDetailsLivedAbroadForm(GOVUKForm):
    """
    GOV.UK form for
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    options = (
        (True, 'Yes'),
        (False, 'No')
    )

    lived_abroad = forms.ChoiceField(
        label='Have you lived outside of the UK in the last 5 years?',
        choices=options,
        widget=InlineRadioSelect,
        required=True,
        error_messages={'required': 'Please select if you have lived outside of the UK in the last 5 years'}
    )
