from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from nanny.utilities import app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyFormView
from your_children_app.forms.your_children_addresses import YourChildrenLivingWithYouForm
from your_children_app.utils import child_lives_with_applicant_handling


class YourChildrenAddressesView(NannyFormView):
    """
    Form view to render the 'your children's addresses' page
    """
    template_name = "your-children-addresses.html"
    form_class = YourChildrenLivingWithYouForm

    def get_context_data(self, **kwargs):
        """
        Method for handling GET requests to the 'your children addresses' page
        """
        application_id = self.request.GET["id"]

        context = {
            'application_id': application_id,
            'id': application_id,
        }
        kwargs.update(context)

        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        app_id = self.request.GET.get('id')
        kwargs['id'] = app_id

        return kwargs

    def form_valid(self, form):
        """
        Method for handling a POST request from the 'your children addresses' page
        """
        application_id = app_id_finder(self.request)

        api_response = NannyGatewayActions().list(
            'your-children', params={'application_id': application_id, 'ordering': 'date_created'}
        )

        # Define a list of children from the API response, ordered by the date they were created by the applicant
        children = api_response.record

        for child in children:
            child_lives_with_applicant_handling(application_id, child, form, api_response)

        # Create a list of children who do not live with the applicant
        children_not_living_with_applicant = [child for child in children if not child['lives_with_applicant'] and
                                              child['street_line1'] is '' or not child['street_line1']]

        # If any children do not live with the applicant, the child address sub-task must be presented
        if len(children_not_living_with_applicant) > 0:
            app_api_response = NannyGatewayActions().read('application', params={'application_id': application_id})
            if app_api_response.status_code == 200:
                record = app_api_response.record
                record['your_children_status'] = 'IN_PROGRESS'
                NannyGatewayActions().put('application', params=record)
            # Child number is defined by the first child added by the applicant as it is ordered by date created
            child_number = children_not_living_with_applicant[0]['child']

            return HttpResponseRedirect(reverse('your-children:Your-Children-Postcode') + '?id=' +
                                        application_id + '&child=' + str(child_number))

        # If all the children live with the applicant, return the summary table and skip the address selection
        else:
            app_api_response = NannyGatewayActions().read('application', params={'application_id': application_id})
            if app_api_response.status_code == 200:
                record = app_api_response.record
                record['your_children_status'] = 'IN_PROGRESS'
                NannyGatewayActions().put('application', params=record)
            return HttpResponseRedirect(reverse('your-children:Your-Children-Summary') + '?id=' +
                                        application_id)
