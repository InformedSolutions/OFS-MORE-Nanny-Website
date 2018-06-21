from django import forms

from govuk_forms.forms import GOVUKForm


class AcccountSelectionForm(GOVUKForm):
    """
    GOV.UK form for 'Account-Selction' page.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    options = (
        ('new', 'Start a new application'),
        ('existing', 'Go back to your application')
    )

    account_selection = forms.ChoiceField(label='', choices=options,
                                          widget=forms.RadioSelect, required=True,
                                          error_messages={'required': 'Please select one'})
