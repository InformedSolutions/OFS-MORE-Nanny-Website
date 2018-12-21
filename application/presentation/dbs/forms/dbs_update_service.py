from django import forms

from govuk_forms.widgets import InlineRadioSelect

from application.presentation.utilities import NannyForm


class DBSUpdateServiceForm(NannyForm):
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

    on_dbs_update_service = forms.ChoiceField(
            label='Are you on the DBS update service?',
            choices=options,
            widget=InlineRadioSelect,
            required=True,
            error_messages={'required': 'Please say if you are on the DBS update service'}
    )
