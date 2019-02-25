from django import forms

from govuk_forms.widgets import NumberInput, InlineRadioSelect

from application.presentation.utilities import NannyForm
from application.services.dbs import read_dbs, dbs_date_of_birth_no_match
from application.services.db_gateways import NannyGatewayActions


class DBSNumberFormFieldMixin(forms.Form):
    """
    Mixin for the 'DBS certificate number' ChoiceField.
    """
    # Overrides standard NumberInput widget too give wider field
    widget_instance = NumberInput()
    widget_instance.input_classes = 'form-control form-control-1-4'

    dbs_number = forms.IntegerField(
        label='DBS certificate number',
        help_text='12-digit number on your certificate',
        error_messages={
            'required': 'Please enter your DBS certificate number',
        },
        widget=widget_instance,
    )

    def clean_dbs_number(self):
        """
        DBS certificate number validation
        :return: integer
        """
        # is_valid() call strips leading 0 required by DBS number. Use raw str input from user instead of cleaned_data.
        dbs_number = self.data['dbs_number']
        if len(str(dbs_number)) != 12:
            raise forms.ValidationError('Check your certificate: the number should be 12 digits long')
        application_id = self.initial['application_id']
        response = read_dbs(dbs_number)
        if response.status_code == 200:
            app_details = NannyGatewayActions().read('applicant-personal-details', {'application_id': application_id})
            if dbs_date_of_birth_no_match(response.record, app_details.record):
                raise forms.ValidationError(
                    'Check your DBS certificate. The number you entered does not match your number held by DBS.')
        return dbs_number


class CriminalCautionsAndConvictionsFormFieldMixin(forms.Form):
    """
    Mixin for the 'Do you have any criminal cautions or convictions?' ChoiceField.
    """
    convictions_choices = (
        (True, 'Yes'),
        (False, 'No')
    )

    convictions = forms.ChoiceField(
        label='Do you have any criminal cautions or convictions?',
        choices=convictions_choices,
        error_messages={
            'required': 'Please say if you have any criminal cautions or convictions',
        },
        widget=InlineRadioSelect
    )


class NonCapitaDBSDetailsForm(DBSNumberFormFieldMixin, NannyForm):
    """
    GOV.UK form for the Captia DBS Details Page
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem on this page'
    auto_replace_widgets = True


class CaptiaDBSDetailsForm(DBSNumberFormFieldMixin, NannyForm):
    """
    GOV.UK form for the Non-Capita DBS Details Page
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem on this page'
    auto_replace_widgets = True



