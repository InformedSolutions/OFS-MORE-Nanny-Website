from django import forms

from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import CheckboxSelectMultiple


class TypeOfChildcareTrainingForm(GOVUKForm):
    """
    GOV.UK form for 'Type-Of-Course' page.
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'error-summary.html'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True

    options = (
        ('level_2_training', 'Childcare qualification (level 2 or higher)'),
        ('common_core_training', 'Training in common core skills'),
        ('no_training', 'None')
    )

    childcare_training = forms.MultipleChoiceField(label='', choices=options,
                                                  widget=CheckboxSelectMultiple, required=True,
                                                  error_messages={'required': 'Please select the type of childcare course you have completed'},
                                                  help_text="Select all that apply")

    def clean_childcare_training(self):
        data = self.cleaned_data['childcare_training']

        if 'no_training' in data and len(data) >= 2:
            raise forms.ValidationError('Please select types of courses or none')
        return data

    def __init__(self, *args, **kwargs):
        super(TypeOfChildcareTrainingForm, self).__init__(*args, **kwargs)
        initial_vals = []

        try:
            for option in self.options:
                if kwargs['initial'][option[0]]:
                    initial_vals.append(option[0])
            self.fields['childcare_training'].initial = initial_vals
        except KeyError:  # If they're loading the form for the first time, supply no initial values.
            pass
