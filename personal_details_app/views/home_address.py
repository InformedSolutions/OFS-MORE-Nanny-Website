from coreapi.exceptions import ErrorMessage

from .BASE import *
from ..forms.home_address import HomeAddressForm, HomeAddressLookupForm, HomeAddressManualForm
from ..utils import app_id_finder
from ..address_helper import *
from django.http import HttpResponseRedirect
from django.urls import reverse

from nanny_gateway import NannyGatewayActions


class PersonalDetailHomeAddressView(BaseFormView):

    template_name = 'personal-details-home-address.html'
    form_class = HomeAddressForm
    success_url = 'personal-details:Personal-Details-Select-Address'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['id'] = app_id_finder(self.request)
        return context

    def form_valid(self, form):
        application_id = app_id_finder(self.request)
        postcode = form.cleaned_data['postcode']

        # update the address record if it already existed
        try:
            address_record = NannyGatewayActions().read('applicant-home-address', params={'application_id': application_id})
            address_record['postcode'] = postcode
            NannyGatewayActions().patch('applicant-home-address', address_record)

        # create the address record if it didn't exist
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                personal_details_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id})
                address_record = {
                    'application_id': application_id,
                    'personal_detail_id': personal_details_record['personal_detail_id'],
                    'postcode': postcode
                }
                NannyGatewayActions().create('applicant-home-address', params=address_record)
            else:
                raise e

        return super().form_valid(form)


class PersonalDetailSelectAddressView(BaseFormView):

    template_name = 'personal-details-home-address-lookup.html'
    form_class = HomeAddressLookupForm
    success_url = 'personal-details:Personal-Details-Address-Summary'

    def form_valid(self, form):
        app_id = app_id_finder(self.request)
        selected_address_index = form.cleaned_data['address']

        record = NannyGatewayActions().read('applicant-home-addresss', params={'application_id': app_id})
        selected_address = AddressHelper.get_posted_address(selected_address_index, record['postcode'])
        record['street_line1'] = selected_address['line1']
        record['street_line2'] = selected_address['line2']
        record['town'] = selected_address['townOrCity']
        record['county'] = None
        record['postcode'] = selected_address['postcode']
        NannyGatewayActions().patch('applicant-home-address', params=record)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        app_id = app_id_finder(self.request)

        record = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
        postcode =record['postcode']
        kwargs['postcode'] = postcode
        kwargs['id'] = app_id
        address_choices = AddressHelper.create_address_lookup_list(postcode)
        self.initial['choices'] = address_choices

        return super(PersonalDetailSelectAddressView, self).get_context_data(**kwargs)


class PersonalDetailManualAddressView(BaseFormView):

    template_name = 'personal-details-home-address-manual.html'
    success_url = 'personal-details:Personal-Details-Address-Summary'
    form_class = HomeAddressManualForm

    def get_initial(self):
        initial = super().get_initial()
        app_id = app_id_finder(self.request)

        try:
            record = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
            initial['street_line1'] = record['street_line1']
            initial['street_line2'] = record['street_line2']
            initial['town'] = record['town']
            initial['county'] = record['county']
            initial['postcode'] = record['postcode']
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                pass
            else:
                raise e

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        context['id'] = app_id
        return context

    def form_valid(self, form):
        app_id = app_id_finder(self.request)
        street_line1 = form.cleaned_data['street_line1']
        street_line2 = form.cleaned_data['street_line2']
        town = form.cleaned_data['town']
        county = form.cleaned_data['county']
        postcode = form.cleaned_data['postcode']

        # update the address record if it already existed
        try:
            address_record = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
            address_record['street_line1'] = street_line1
            address_record['street_line2'] = street_line2
            address_record['town'] = town
            address_record['county'] = county
            address_record['postcode'] = postcode
            NannyGatewayActions().patch('applicant-home-address', address_record)

        # create the address record if it didn't exist
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                personal_details_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': app_id})
                address_record = {
                    'application_id': app_id,
                    'personal_detail_id': personal_details_record['personal_detail_id'],
                    'street_line1': street_line1,
                    'street_line2': street_line2,
                    'town': town,
                    'county': county,
                    'postcode': postcode,
                }
                NannyGatewayActions().create('applicant-home-address', params=address_record)
            else:
                raise e

        return super().form_valid(form)


class PersonalDetailSummaryAddressView(BaseTemplateView):

    template_name = 'address-details.html'
    success_url = 'personal-details:Personal-Details-Lived-Abroad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        address_record = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
        context['address'] = AddressHelper.format_address(address_record, ", ")
        context['id'] = app_id
        return context

    def post(self, request):
        """
        Handle post requests to the guidance page.
        """
        app_id = app_id_finder(request)
        return HttpResponseRedirect(reverse('personal-details:Personal-Details-Lived-Abroad') + "?id=" + app_id)
