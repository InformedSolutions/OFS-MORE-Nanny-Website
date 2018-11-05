from datetime import datetime
from django.shortcuts import render
from your_children_app.forms.your_children_details_form import YourChildrenDetailsForm
from nanny.utilities import app_id_finder
from nanny.base_views import NannyFormView
import uuid
from ..utils import *
from nanny.db_gateways import NannyGatewayActions


class YourChildrenDetailsView(NannyFormView):
    """
    Template view to  render the your children details view
    """
    def get(self, request, *args, **kwargs):
        application_id = request.GET["id"]
        api_response = NannyGatewayActions().list(
            'your-children', params={'application_id': application_id, 'ordering': 'date_created'})
        number_of_children_present_in_querystring = request.GET.get('children') is not None

        if number_of_children_present_in_querystring:
            number_of_children = int(request.GET["children"])
        else:
            if api_response.status_code == 200:
                number_of_children = len(api_response.record)
            else:
                number_of_children = 0

        remove_request_querystring_present = (request.GET.get('remove') is not None)
        child_to_remove = 0
        remove_button = True

        if remove_request_querystring_present:
            child_to_remove = str(request.GET.get('remove'))

        # If there are no children, set the number to 1 to initialise the first form
        if number_of_children == 0:
            number_of_children = 1

        # Disable the 'remove' button if there is only one child
        if number_of_children == 1:
            remove_button = False

        # Remove the child from the record if the 'Remove' button is used, then update the
        # 'child' number based on the creation date of the record
        if remove_request_querystring_present and child_to_remove != '0':
            remove_child(child_to_remove, application_id)
            assign_child_numbers(api_response)

        # Generate a list of forms that will be iterated through when the page is initialised
        form_list = []

        for i in range(1, number_of_children + 1):

            try:
                child_id = NannyGatewayActions().list('your-children', params={
                          'application_id': str(application_id),
                          'ordering': 'date_created'}).record[i-1]['child_id']
            except (IndexError, AttributeError):
                child_id = None

            form = YourChildrenDetailsForm(
                id=application_id,
                child_id=child_id,
                child=i,
                prefix=i,
            )

            # ARC return/flagging here

            # Add each form to the form list
            form_list.append(form)

        variables = {
            'form_list': form_list,
            'application_id': application_id,
            'id': application_id,
            'number_of_children': number_of_children,
            'add_child': number_of_children + 1,
            'remove_child': number_of_children - 1,
            'remove_button': remove_button,
        }

        return render(request, 'your-children-details.html', variables)

    def post(self, request, *args, **kwargs):
        """
        POST handler for the 'Your children details' page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # Pull information out of the request
        application_id = request.POST["id"]
        number_of_children = request.POST["children"]

        remove_button = True

        # Initialise the page with an empty child representation
        if number_of_children == 0:
            number_of_children = 1

        if number_of_children == 1:
            remove_button = False

        form_list = []
        valid_list = []

        for i in range(1, int(number_of_children) + 1):

            try:
                child_id = NannyGatewayActions().list('your-children', params={
                          'application_id': str(application_id),
                          'ordering': 'date_created'}).record[i-1]['child_id']
            except (IndexError, AttributeError):
                child_id = None

            form = YourChildrenDetailsForm(request.POST,
                                           id=application_id,
                                           child_id=child_id,
                                           child=i,
                                           prefix=i,
                                           )

            form_list.append(form)
            form.error_summary_title = "There was a problem with your children's details"

            api_response = NannyGatewayActions().read('application', params={
                'application_id': application_id})

            if api_response.record['application_status'] == 'FURTHER_INFORMATION':
                form.error_summary_template_name = 'returned-error-summary.html'
                form.error_summary_title = "There was a problem with your children's details"

            if form.is_valid():
                application_id = app_id_finder(self.request)
                # Get child_id if the child exists within the record

                first_name = form.cleaned_data['first_name']
                middle_names = form.cleaned_data['middle_names']
                last_name = form.cleaned_data['last_name']
                date_of_birth = form.cleaned_data['date_of_birth']

                if child_id:
                    # Update an existing child's record
                    api_response = NannyGatewayActions().read('your-children', params={'child_id': child_id})

                    api_response.record['first_name'] = first_name
                    api_response.record['middle_names'] = middle_names
                    api_response.record['last_name'] = last_name
                    api_response.record['birth_day'] = date_of_birth.day
                    api_response.record['birth_month'] = date_of_birth.month
                    api_response.record['birth_year'] = date_of_birth.year

                    NannyGatewayActions().put('your-children', params=api_response.record)

                else:
                    NannyGatewayActions().create(
                        'your-children',
                        params={
                            'application_id': application_id,
                            'child_id': uuid.uuid4(),
                            'date_created': datetime.datetime.today(),
                            'first_name': first_name,
                            'middle_names': middle_names,
                            'last_name': last_name,
                            'birth_day': date_of_birth.day,
                            'birth_month': date_of_birth.month,
                            'birth_year': date_of_birth.year,
                        }
                    )

                valid_list.append(True)

            # form is not valid
            else:
                valid_list.append(False)

        application = NannyGatewayActions().read('application', params={'application_id': application_id})

        # Define the 'child' number based on the creation date of the record. Should account for added and removed
        api_response = NannyGatewayActions().list(
            'your-children', params={'application_id': application_id, 'ordering': 'date_created'})

        if api_response.status_code == 200:
            assign_child_numbers(api_response)

        if 'submit' in request.POST:

            if all(valid_list):
                return HttpResponseRedirect(reverse('your-children:Your-Children-addresses') + '?id=' + application_id)

            # If there is an invalid form
            else:
                variables = {
                    'form_list': form_list,
                    'application_id': application_id,
                    'id': application_id,
                    'number_of_children': number_of_children,
                    'add_child': int(number_of_children) + 1,
                    'remove_child': int(number_of_children) - 1,
                    'remove_button': remove_button,
                    'your_children_status': application.record['your_children_status']
                }

                return render(request, 'your-children-details.html', variables)

        if 'add_person' in request.POST:

            if False not in valid_list:
                variables = {
                    'application_id': application_id,
                    'your_children_status': application.record['your_children_status'],
                    'id': application_id,
                }
                add_child = int(number_of_children) + 1
                add_child_string = str(add_child)
                return HttpResponseRedirect(reverse('your-children:Your-Children-Details') + '?id=' +
                                            application_id + '&children=' + add_child_string + '&remove=0#person'
                                            + add_child_string, variables)
            # If there is an invalid form
            else:
                variables = {
                    'form_list': form_list,
                    'application_id': application_id,
                    'id': application_id,
                    'number_of_children': number_of_children,
                    'add_adult': int(number_of_children) + 1,
                    'remove_child': int(number_of_children) - 1,
                    'remove_button': remove_button,
                    'your_children_status': application.record['your_children_status']
                }

                return render(request, 'your-children-details.html', variables)
