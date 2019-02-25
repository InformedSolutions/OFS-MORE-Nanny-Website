from django import forms

from application.presentation.utilities import NannyForm
from application.services.ConditionalPostChoiceWidget import ConditionalPostInlineRadioSelect


class PersonalDetailsYourChildrenForm(NannyForm):
    """
    GOV.UK form for specifying whether the applicant is known to social services in regards to their own children.
    """
    field_label_classes = 'form-label-bold'
    error_summary_title = 'There was a problem'
    auto_replace_widgets = True
    reveal_conditionally = {'known_to_social_services': {True: 'reasons_known_to_social_services'}}

    options = (
        (True, 'Yes'),
        (False, 'No')
    )

    ERROR_MESSAGE_PROVIDE_CHOICE_FIELD = 'Please say if you are known to council social services in regards to your own children'
    ERROR_MESSAGE_PROVIDE_REASON = "You must tell us why"

    known_to_social_services = forms.ChoiceField(
        label='Are you known to council social services in regards to your own children?',
        choices=options,
        widget=ConditionalPostInlineRadioSelect,
        required=True,
        error_messages={'required': ERROR_MESSAGE_PROVIDE_CHOICE_FIELD}
    )

    reasons_known_to_social_services = forms.CharField(
        label="Tell us why",
        widget=forms.Textarea,
        required=True,
        error_messages={'required': ERROR_MESSAGE_PROVIDE_REASON}
    )

    def clean(self):
        cleaned_data = self.cleaned_data

        known_to_social_services = cleaned_data.get('known_to_social_services', None)
        reasons_known_to_social_services = cleaned_data.get('reasons_known_to_social_services', None)

        known_to_social_services_bool = known_to_social_services == 'True'

        if known_to_social_services_bool is True and reasons_known_to_social_services == '':
            self.add_error('reasons_known_to_social_services', self.ERROR_MESSAGE_PROVIDE_REASON)
        elif known_to_social_services_bool is False:
            cleaned_data['reasons_known_to_social_services'] = ''

        # Update cleaned_data
        cleaned_data['known_to_social_services'] = known_to_social_services_bool
        return cleaned_data