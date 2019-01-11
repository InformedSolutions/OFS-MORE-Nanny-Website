from django import forms
from govuk_forms.widgets import InlineRadioSelect

from application.presentation.utilities import NannyForm


class ChildcareLocationForm(NannyForm):
    """
    GOV.UK form for 'Childcare-Location' page.
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True
    options = (
        ('True', 'Yes'),
        ('False', 'No')
    )
    both_work_and_home_address = forms.ChoiceField(choices=options,
                                                   label='Will you work and live at the same address?',
                                                   required=True,
                                                   widget=InlineRadioSelect,
                                                   error_messages={
                                                       'required': "Please say if you'll work and live at the same address"}
                                                   )

    def __init__(self, *args, **kwargs):
        super(ChildcareLocationForm, self).__init__(*args, **kwargs)

        if 'both_work_and_home_address' in kwargs['initial'] and 'home_address_id' in kwargs['initial']:
            self.fields['both_work_and_home_address'].initial = kwargs['initial']['both_work_and_home_address']
            self.pk = kwargs['initial']['home_address_id']
        self.field_list = ['both_work_and_home_address']
