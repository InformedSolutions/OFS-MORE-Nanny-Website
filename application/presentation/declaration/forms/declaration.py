from django import forms
from govuk_forms.forms import GOVUKForm


class DeclarationForm(GOVUKForm):
    """
    GOV.UK form for the Declaration: declaration page
    """
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    confirm_declare = forms.BooleanField(label='I confirm', required=True,
                                        error_messages={
                                            'required': 'You must confirm everything on this page to continue'})