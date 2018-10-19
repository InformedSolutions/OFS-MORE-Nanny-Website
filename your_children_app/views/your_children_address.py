from django.http import HttpResponseRedirect
from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView


class YourChildrenAddressView(NannyTemplateView):
    """
    Template view to  render the your children postcode lookup view
    """
    template_name = "your-children-address.html"
    success_url_name = 'your-children:Your-Children-address-lookup'

    def post(self, request):

        app_id = app_id_finder(self.request)
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('your-children:Your-Children-address-lookup', get={'id': app_id}))


class YourChildrenAddressLookupView(NannyTemplateView):
    """
    Template view to  render the your children address selection view
    """
    template_name = "your-children-address-lookup.html"
    success_url_name = 'your-children:Your-Children-Summary'

    def post(self, request):

        app_id = app_id_finder(self.request)
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('your-children:Your-Children-Summary', get={'id': app_id}))


class YourChildrenManualAddressView(NannyTemplateView):
    """
    Template view to  render the your children details view
    """
    template_name = "your-children-address-manual.html"
    success_url_name = 'your-children:Your-Children-Summary'

    def post(self, request):

        app_id = app_id_finder(self.request)
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('your-children:Your-Children-Summary', get={'id': app_id}))
