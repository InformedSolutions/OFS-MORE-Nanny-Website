from django import forms
from govuk_forms.forms import GOVUKForm


class DeclarationForm(GOVUKForm):
    """
    GOV.UK form for the Declaration: declaration page
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    auto_replace_widgets = True

    follow_rules = forms.BooleanField(label='I must follow the rules in the register', required=True,
                                      error_messages={'required':
                                        'Confirm you understand that you must follow the rules in the register'})
    share_info_declare = forms.BooleanField(label='Ofsted will share information with other organisations',
                                            required=True,
                                            error_messages={
                                                'required': 'Confirm you understand Ofsted will share information with other organisations'})
    information_correct_declare = forms.BooleanField(label='the information I have given is correct', required=True,
                                                     error_messages={
                                                         'required': 'Confirm that the information you have given is correct'})
    change_declare = forms.BooleanField(label='I will tell Ofsted if this information changes', required=True,
                                        error_messages={
                                            'required': 'Confirm that you will tell Ofsted if this information changes'})