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

        application_id = app_id_finder(self.request)

        # instigate the associated form
        super(YourChildrenLivingWithYouForm, self).__init__(*args, **kwargs)

        api_response = NannyGatewayActions().read('your-children', params={'application_id': application_id})

        # Fetch selection options (child names) and order by the order they were added in the details section
        children = sorted(api_response.record, key=lambda child_in_response: child_in_response[2])

        # Create outer tuple to hold tuple of child names and ints
        select_options = ()
        previous_selections = []

        # Iterate each child and push to tuple tuple
        for child in children:
            # If the child lives with the applicant
                # Add the child to the previous selections list

            # Add the child's full name to the select options list

        # Add none option to the end of the list, post loop
        select_options += (('none', 'None'),)

        # If previous address selections are empty but addresses are present, it is safe to assume



    def clean_children_living_with_applicant_selection(self):
        """

        :return:
        """
