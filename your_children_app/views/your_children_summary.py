from django.http import HttpResponseRedirect
from django.shortcuts import render

from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView
from your_children_app.forms.your_children_summary_form import YourChildrenSummaryForm


class YourChildrenSummaryView(NannyTemplateView):
    """
    From view to handle GET and POST requests to the 'Your Children' task summary view
    """
    def get(self, request, *args, **kwargs):
        """
        Method for handling GET requests to the 'Your Children' summary page
        """
        application_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('application', params={'application_id': application_id})
        form = YourChildrenSummaryForm()

        # Form error summary initialisation from ARC return
        if api_response['application_status'] == 'FURTHER_INFORMATION':
            form.error_summary_template_name = 'returned-error-summary.html'
            form.error_summary_title = "There was a problem"

        # Define the new API request to list all children related to the applicant
        api_response = NannyGatewayActions().list(
            'your-children', params={'application_id': application_id, 'ordering': 'date_created'}
        )

        children = api_response.record
        child_table_list = []

        # Create a summary table for
        for child in children:
            child_table = create_child_table(child) #TODO: Add and convert the helper method
            child_table_list.append(child_table)

        child_table_list = #TODO: Convert James's helper code here to return list of tables for applicant children

        for table in child_table_list:
            for row in table.get_row_list():
                if row.data_name == 'address' and row.value == #TODO: Update this with helper methods and matching text
                    row.back_link = 'your-children:Your-Children-addresses'

        children_living_with_applicant_table = #TODO: Add helper function to create table

        # Add the generated tables together to display both tables in the summary view
        table_list = [children_living_with_applicant_table] + child_table_list

        variables = {
            'page_title': 'Check your answers: your children',
            'form': form,
            'application_id': application_id,
            'table_list': table_list,
            'your_children_status': api_response['application_status'],
        }

        variables = submit_link_setter(variables, table_list, 'your_children', application_id) #TODO: Add helper method

        return render(request, 'generic-summary-template.html', variables)

    def post(self, request, *args, **kwargs):
        """
        Method for handling POST requests to the 'Your Children' task summary page
        """

        app_id = app_id_finder(self.request)
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})

        if app_api_response.status_code == 200:
            # Update the task status to 'Done'
            record = app_api_response.record
            record['your_children_status'] = 'COMPLETED'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('Task-List', get={'id': app_id}))