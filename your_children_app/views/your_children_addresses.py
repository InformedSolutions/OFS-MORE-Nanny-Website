from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView
from your_children_app.forms.your_children_addresses import YourChildrenLivingWithYouForm


class YourChildrenAddressesView(NannyTemplateView):
    """

    """

    def get(self, request, *args, **kwargs):
        """
        Method for handling GET requests to the 'your children addresses' page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        application_id = app_id_finder(self.request)
        form = YourChildrenLivingWithYouForm(id=application_id)

        variables = {
            'form': form,
            'application_id': application_id,
        }

        return render(request, "your-children-addresses.html", variables)

    def post(self, request, *args, **kwargs):
        """
        Method for handling a POST request from the 'your children addresses' page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        application_id = app_id_finder(self.request)
        form = YourChildrenLivingWithYouForm(request.POST, id=application_id)
        api_response = NannyGatewayActions().read('your-children', params={'application_id': application_id})

        # Form does not pass validation
        if not form.is_valid():
            variables={
                'form': form,
                'application_id': application_id,
            }

            return render(request, "your-children-addresses.html", variables)

        # Children selected in the list should be assigned the applicants address
        children = api_response.record

        for child in children:
            # Append True or False to the child's live's with applicant status
            child['lives_with_applicant'] = str(child['child']) in form.cleaned_data[
                'children_living_with_applicant_selection']

            if child['lives_with_applicant']:
                # get the existing address of the applicant from the personal details records
                applicant_record = NannyGatewayActions().read('applicant_home_address', params={
                    'application_id': application_id
                })

                # Define the address details for the child model
                api_response.record['street_line1'] = applicant_record['street_line1']
                api_response.record['street_line2'] = applicant_record['street_line2']
                api_response.record['town'] = applicant_record['town']
                api_response.record['county'] = applicant_record['county']
                api_response.record['country'] = applicant_record['country']
                api_response.record['postcode'] = applicant_record['postcode']

                # Append the existing children, that are ticked in the form, with the address of the applicant
                if api_response == 200:
                    NannyGatewayActions().patch('your_children_details', params=api_response.record)

                # The child record should always exist at this point, following the creation in child details
                else:
                    raise ValueError('The API did not respond as expected')

        # Create a list of children who do not live with the applicant
        children_not_living_with_applicant = [child for child in children if children['street_line1'] is None]

        # If any children do not live with the applicant, the child address sub-task must be presented
        if len(children_not_living_with_applicant) > 0:
            child_number = children_not_living_with_applicant[0]['child']

            return HttpResponseRedirect(reverse('your-children:Your-Children-address') + '?id=' +
                                        application_id + '&child=' + str(child_number))

        # If all the children live with the applicant, return the summary table and skip the address selction
        else:
            return HttpResponseRedirect(reverse('your-children:Your-Children-Summary') + '?id=' +
                                        application_id)
