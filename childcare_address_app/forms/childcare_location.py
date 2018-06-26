from django import forms

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import InlineRadioSelect


class ChildcareLocationForm(GOVUKForm):
    """
    GOV.UK form for 'Childcare-Location' page.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True
    options = (
        ('True', 'Yes'),
        ('False', 'No')
    )
    home_address = forms.ChoiceField(choices=options,
                                               label='Is your work address the same as your home address?',
                                               required=True,
                                               widget=InlineRadioSelect,
                                               error_messages={'required': 'Please answer yes or no'})
