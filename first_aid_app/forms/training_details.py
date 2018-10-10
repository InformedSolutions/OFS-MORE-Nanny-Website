from django import forms

from nanny.utilities import NannyForm

from first_aid_app.widgets.customfields import CustomSplitDateField


class FirstAidTrainingDetailsForm(NannyForm):
    """
    GOV.UK form for the First aid training: details page
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    auto_replace_widgets = True
    error_summary_title = 'There was a problem'

    training_organisation = forms.CharField(
        label='Training organisation',
        error_messages={
            'required': 'Please enter the name of the training organisation',
        }
    )

    course_title = forms.CharField(
        label='Title of training course',
        error_messages={
            'required': 'Please enter the title of the course',
        }
    )

    course_date = CustomSplitDateField(
        label='Date you completed course',
        help_text='For example, 31 03 2016',
        error_messages={'required': 'Please enter the full date, including the day, month and year'},
        
    )

    def clean_first_aid_training_organisation(self):
        organisation = self.cleaned_data['first_aid_training_organisation']
        if len(organisation) > 50:
            raise forms.ValidationError('The name of the training organisation must be under 50 characters')

        return organisation

    def clean_title_of_training_course(self):
        title = self.cleaned_data['title_of_training_course']
        if len(title) > 50:
            raise forms.ValidationError('The title of the course must be under 50 characters long')

        return title
