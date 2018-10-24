from django import forms
from govuk_forms.widgets import CheckboxSelectMultiple
from nanny import NannyForm, app_id_finder, NannyGatewayActions


class YourChildrenLivingWithYouForm(NannyForm):
    """
    GOV.UK form for the your children addresses page
    """
    field_label_classes = 'form-label-bold'
    error_summary_template_name = 'standard-error-summary.html'
    error_summary_title = 'There was a problem on this page'
    auto_replace_widgets = True

    # Define the form characteristics
    children_living_with_applicant_selection = forms.MultipleChoiceField(
        label='Which of your children live with you?',
        widget=CheckboxSelectMultiple, required=True, error_messages={
            'required': 'Please say if any of your children live with you'}, help_text="Tick all that apply")

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """

        self.application_id_local = kwargs.pop('id')
        child_id = kwargs.pop('child_id')

        # instigate the associated form
        super(YourChildrenLivingWithYouForm, self).__init__(*args, **kwargs)

        # Read the 'your children' endpoint to return details of the children
        api_response = NannyGatewayActions().list(
            'your-children', params={'application_id': self.application_id_local, 'ordering': 'child'}
        )

        children = api_response.record



        # Create outer tuple to hold tuple of child names and ints
        select_options = ()
        previous_selections = []

        # Iterate each child and push to tuple tuple
        for child in children:
            if child['lives_with_applicant']:
                # Add the child to the previous selections list
                previous_selections.append(str(child['child']))

            # Add the child's full name to the select options list
            select_options += (str(child['child'], child['first_name']))

        # Add none option to the end of the list, post loop
        select_options += (('none', 'None'),)

        # If previous address selections are empty but addresses are present, it is safe to assume
        prior_child_address_count = len([child for child in children if child['street_line1'] is not None])

        if (len(previous_selections) == 0) and (prior_child_address_count > 0):
            previous_selections.append('none')

        self.fields['children_living_with_applicant_selection'].choices = select_options
        self.fields['children_living_with_applicant_selection'].initial = previous_selections

        self.field_list = ['children_living_with_applicant_selection']
        self.pk = self.application_id_local

    def clean_children_living_with_applicant_selection(self):
        """
        Ensures that the form does not pass validation when 'none' is selected as well as children
        """
        selections = self.cleaned_data['children_living_with_applicant_selection']

        if len(selections) > 1 and 'none' in selections:
            raise forms.ValidationError('Please select your children''s names or none.')

        return selections
