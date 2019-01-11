from django import forms

from govuk_forms.widgets import InlineRadioSelect

from application.presentation.utilities import NannyForm


class PersonalDetailsYourChildrenForm(NannyForm):
    """
    GOV.UK form for specifying whether or not the applicant has children of their own who are under 16 years old.
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    options = (
        (True, 'Yes'),
        (False, 'No')
    )

    your_children = forms.ChoiceField(
        label='Do you have children of your own under 16?',
        choices=options,
        widget=InlineRadioSelect,
        required=True,
        error_messages={'required': 'Please say if you have children of your own under 16'}
    )
