from django import forms

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import InlineRadioSelect

from nanny.db_gateways import NannyGatewayActions


class WhereYouWorkForm(GOVUKForm):
    """
    GOV.UK form for 'Where-You-Work' page.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True
    options = (
        ('True', 'Yes'),
        ('False', 'No')
    )
    address_to_be_provided = forms.ChoiceField(choices=options,
                                               label='Do you know where you will be working?', required=True,
                                               widget=InlineRadioSelect,
                                               error_messages=
                                               {'required': 'Please say if you know where you will be working'})

    def __init__(self, *args, **kwargs):
        if 'id' in kwargs['initial']:
            self.application_id_local = kwargs['initial']['id']
        elif 'data' in kwargs and 'id' in kwargs['data']:
            self.application_id_local = kwargs['data']['id']

        super(WhereYouWorkForm, self).__init__(*args, **kwargs)

        if hasattr(self, 'application_id_local'):
            response = NannyGatewayActions().read('application', params={'application_id': self.application_id_local})
            record = response.record

            self.fields['address_to_be_provided'].initial = record['address_to_be_provided']
            self.pk = self.application_id_local
            self.field_list = ['address_to_be_provided']
