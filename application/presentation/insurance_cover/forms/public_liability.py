from django import forms

from application.presentation.utilities import NannyForm
from govuk_forms.widgets import InlineRadioSelect


class PublicLiabilityForm(NannyForm):
    """
    GOV.UK form for 'Public Liability' page.
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True
    options = (
        ('True', 'Yes'),
        ('False', 'No')
    )
    public_liability = forms.ChoiceField(choices=options,
                                               label='Do you have public liability insurance?',
                                               required=True,
                                               widget=InlineRadioSelect,
                                               error_messages={'required': 'Please say if you have public liability insurance'})
