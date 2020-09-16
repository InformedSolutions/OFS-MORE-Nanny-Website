from django import forms
from govuk_forms.widgets import RadioSelect

from govuk_forms.forms import GOVUKForm


class AnalyticsCookieSelection(GOVUKForm):
    """
    GOV.UK form for opting in or out of cookies: Cookie Policy page
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem on this page'
    auto_replace_widgets = True

    options = (
        ('opted_in', 'On'),
        ('opted_out', 'Off')
    )

    cookie_selection = forms.ChoiceField(label='', choices=options,
                                         widget=RadioSelect, required=True,
                                         error_messages={
                                             'required': 'Select if you want to allow us to use GA (confirm wording)'})
