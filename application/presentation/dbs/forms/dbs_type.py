from django import forms

from govuk_forms.widgets import InlineRadioSelect

from application.presentation.utilities import NannyForm


class DBSTypeForm(NannyForm):
    """
    GOV.UK form for the 'Lived Abroad' Page
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    options = (
        ('True', 'Yes'),
        ('False', 'No')
    )

    is_ofsted_dbs = forms.ChoiceField(
            label='Do you have an Ofsted DBS check?',
            choices=options,
            widget=InlineRadioSelect,
            required=True,
            error_messages={'required': 'Please say if you have an Ofsted DBS check'}
    )
