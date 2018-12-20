from django import forms

from govuk_forms.widgets import InlineRadioSelect

from nanny.utilities import NannyForm


class PersonalDetailsLivedAbroadForm(NannyForm):
    """
    GOV.UK form for specifying whether or not the applicant has lived abroad in the past 5 years.
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
