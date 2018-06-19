from django import forms

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import CheckboxSelectMultiple


class TypeOfChildcareTrainingForm(GOVUKForm):
    """
    GOV.UK form for 'Type-Of-Course' page.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem on this page'
    auto_replace_widgets = True

    options = (
        ('level2', 'Childcare qualification (level 2 or higher)'),
        ('common_core', 'Training in common core skills'),
        ('none', 'None')
    )

    account_selection = forms.MultipleChoiceField(label='', choices=options,
                                                  widget=CheckboxSelectMultiple, required=True,
                                                  error_messages={'required': 'Please select one'},
                                                  help_text="Select all that apply")
