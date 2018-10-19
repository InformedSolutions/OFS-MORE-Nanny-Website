from django.http import HttpResponseRedirect
from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView


class YourChildrenAddressesView(NannyTemplateView):
    """
    Template view to  render the your children details view
    """
    template_name = "your-children-addresses.html"
    success_url_name = 'your-children:Your-Children-address'
    # form = X

    """
    def get_context_data:
        initial form population, pull in the ID from the API, pull in the children list from the API.
        
        if initial context data does not exist:
            create the records as '' or none that can be populated later, without having to do these within the 
            view of the 'your_children_details
    """

    def post(self, request):


        """



        if a child is 'ticked' within the form:
            assign the applicant address details to the details of the child

        children_with_addresses = child in children where addr['line1'] is not None

        if len(children_with_addresses) = len(children):
            success_url =
            progress to the summary page

        elif len(children_with_addresses) != len(children):
            children_without_addresses = child in children where addr['line1'] is None
            success_url =
            progress to the address details page

        else:
            API Shenanigans
            raise exception

        """

        app_id = app_id_finder(self.request)
        # update task status to be done
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('your-children:Your-Children-address', get={'id': app_id}))
