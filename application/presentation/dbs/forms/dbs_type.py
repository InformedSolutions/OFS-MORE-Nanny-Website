from django import forms

from govuk_forms.widgets import InlineRadioSelect

from application.presentation.utilities import NannyForm
from application.services.ConditionalPostChoiceWidget import ConditionalPostInlineRadioSelect


class DBSTypeForm(NannyForm):
    """
    GOV.UK form for the 'Lived Abroad' Page
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True
    capita_field_name = 'is_ofsted_dbs'
    update_field_name = 'on_dbs_update_service'

    options = (
        ('True', 'Yes'),
        ('False', 'No')
    )

    on_dbs_update_service = forms.ChoiceField(
        label=' Are you on the DBS update service?',
        choices=options,
        widget=InlineRadioSelect,
        required=True,
        error_messages={'required': 'Please say if you are on the DBS Update Service'}
    )

    def __init__(self, *args, **kwargs):
        ask_if_capita = kwargs['initial']['is_ofsted_dbs']
        if not ask_if_capita:
            self.reveal_conditionally = {'is_ofsted_dbs': {'True': self.update_field_name}}
        super().__init__(*args, **kwargs)
        if not ask_if_capita:
            self.fields[self.capita_field_name] = self.get_ofsted_dbs_field_data()


    def get_ofsted_dbs_field_data(self):
        return forms.ChoiceField(
            label='Is it an enhanced check for home-based childcare?',
            choices=self.options,
            widget=ConditionalPostInlineRadioSelect,
            required=True,
            error_messages={'required': 'Please say if you have an enhanced check for home-based childcare'}
        )


