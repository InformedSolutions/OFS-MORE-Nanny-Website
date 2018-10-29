from django.http import HttpResponseRedirect
from django.shortcuts import render

from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions, reverse
from nanny.base_views import NannyFormView
from your_children_app.forms.your_children_address import YourChildrenAddressForm


class YourChildrenPostcodeView(NannyFormView):
    """
    Template view to  render the your children postcode lookup view
    """

    def get(self, request, *args, **kwargs):
        """
        Method to handle get requests to the 'Your Children' postcode lookup page
        """
        application_id = request.GET["id"]
        child = request.GET["child"]
        form = YourChildrenAddressForm(id=application_id, child=child)
        child_record = NannyGatewayActions().list('your-children', params={
            'application_id': application_id,
            'child': str(child),
        }).record[0]

        name = child_record['first_name'] + " " + child_record['last_name']
        variables = {
            'form': form,
            'name': name,
            'application_id': application_id,
            'child': child,
        }

        return render(request, 'your-children-address.html', variables)

    def post(self, request, *args, **kwargs):
        """
        Method to handle post requests from the 'Your Children' postcode lookup page
        """
        application_id = request.POST["id"]
        child = request.POST["child"]
        form = YourChildrenAddressForm(id=application_id, child=child)
        child_record = NannyGatewayActions().list('your-children', params={
            'application_id': application_id,
            'child': str(child),
        }).record[0]

        application_api = NannyGatewayActions().read('application', params={'application_id': application_id})

        if 'postcode-search' in request.POST:

            if form.is_valid():
                # Update child record
                postcode = form.cleaned_data.get('postcode')
                child_record['postcode'] = postcode
                NannyGatewayActions().patch('your-children', params=child_record)

                # Update task status
                if application_api['application_status'] != 'COMPLETED':
                    application_api['application_status'] = 'IN_PROGRESS'

                return HttpResponseRedirect(reverse('your-children:Your-Children-address-lookup')
                                            + '?id=' + application_id + '&child=' + str(child))

            else:
                # Form is not valid
                form.error_summary_title = 'There was a problem with your postcode'

                if application_api['application_status'] == 'FURTHER_INFORMATION':
                    form.error_summary_template_name = 'returned-error-summary.html'
                    form.error_summary_title = 'There was a problem'

                name = child_record['first_name'] + " " + child_record['last_name']

                variables = {
                    'form': form,
                    'name': name,
                    'application_id': application_id,
                    'child': child,
                }

                return render(request, 'your-children-address-lookup.html', variables)


class YourChildrenAddressSelectionView(NannyFormView):
    """
    Template view to  render the your children address selection view
    """
    template_name = "your-children-address-lookup.html"
    success_url_name = 'your-children:Your-Children-Summary'

    def post(self, request, *args, **kwargs):
        app_id = app_id_finder(self.request)
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('your-children:Your-Children-Summary', get={'id': app_id}))


class YourChildrenManualAddressView(NannyFormView):
    """
    Template view to  render the your children details view
    """
    template_name = "your-children-address-manual.html"
    success_url_name = 'your-children:Your-Children-Summary'

    def post(self, request, *args, **kwargs):
        app_id = app_id_finder(self.request)
        app_api_response = NannyGatewayActions().read('application', params={'application_id': app_id})
        if app_api_response.status_code == 200:
            record = app_api_response.record
            record['your_children_status'] = 'IN_PROGRESS'
            NannyGatewayActions().put('application', params=record)

        return HttpResponseRedirect(build_url('your-children:Your-Children-Summary', get={'id': app_id}))
