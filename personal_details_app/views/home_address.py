from ..forms.home_address import HomeAddressForm, HomeAddressLookupForm, HomeAddressManualForm
from ..address_helper import *
from django.http import HttpResponseRedirect
from django.urls import reverse

from nanny.base_views import NannyFormView, NannyTemplateView
from nanny.db_gateways import NannyGatewayActions
from nanny.utilities import app_id_finder


class PersonalDetailHomeAddressView(NannyFormView):
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

        api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': application_id})
        if api_response.status_code == 200:
            address_record = api_response.record
            address_record['postcode'] = postcode
            NannyGatewayActions().put('applicant-home-address', params=address_record)
        else:
            personal_details = NannyGatewayActions().read('applicant-personal-details', params={'application_id': application_id}).record
            NannyGatewayActions().create(
                'applicant-home-address',
                params={
                     'application_id': application_id,
                     'personal_detail_id': personal_details['personal_detail_id'],
                     'postcode': postcode,
                 })

        return super().form_valid(form)

    def get_form(self, form_class=None):
        """
        Use BaseFormView method as opposed to NannyFormView's overridden version, as it is not intended for errors to
        appear on the postcode lookup form.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())


class PersonalDetailSelectAddressView(NannyFormView):
    template_name = 'personal-details-home-address-lookup.html'
    form_class = HomeAddressLookupForm
    success_url = 'personal-details:Personal-Details-Address-Summary'

    def form_valid(self, form):
        app_id = app_id_finder(self.request)
        selected_address_index = form.cleaned_data['home_address']
        api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})

        if api_response.status_code == 200:
            record = api_response.record
            selected_address = AddressHelper.get_posted_address(selected_address_index, record['postcode'])
            record['street_line1'] = selected_address['line1']
            record['street_line2'] = selected_address['line2']
            record['town'] = selected_address['townOrCity']
            record['county'] = None
            record['postcode'] = selected_address['postcode']
            NannyGatewayActions().put('applicant-home-address', params=record)  # Update entire record.

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PersonalDetailSelectAddressView, self).get_context_data(**kwargs)
        app_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})

        if api_response.status_code == 200:
            postcode = api_response.record['postcode']
            context['postcode'] = postcode
            context['id'] = app_id
            address_choices = AddressHelper.create_address_lookup_list(postcode)
            self.initial['choices'] = address_choices

        return context

    def get_form(self, form_class=None):
        """
        Use BaseFormView method as opposed to NannyFormView's overridden version, as it is not intended for errors to
        appear on the postcode lookup form.
        If making a POST request, however, we still need to remove the flags.
        """
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())

        if self.request.method == 'POST':
            form.remove_flags(self.request.GET['id'])

        return form


class PersonalDetailManualAddressView(NannyFormView):
    template_name = 'personal-details-home-address-manual.html'
    success_url = 'personal-details:Personal-Details-Address-Summary'
    form_class = HomeAddressManualForm

    def get_initial(self):
        initial = super().get_initial()
        app_id = app_id_finder(self.request)

        api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
        if api_response.status_code == 200:
            initial['street_line1'] = api_response.record['street_line1']
            initial['street_line2'] = api_response.record['street_line2']
            initial['town'] = api_response.record['town']
            initial['county'] = api_response.record['county']
            initial['postcode'] = api_response.record['postcode']

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        context['id'] = app_id
        return context

    def form_valid(self, form):
        app_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
        street_line1 = form.cleaned_data['street_line1']
        street_line2 = form.cleaned_data['street_line2']
        town = form.cleaned_data['town']
        county = form.cleaned_data['county']
        postcode = form.cleaned_data['postcode']

        # update the address record if it already existed
        if api_response.status_code == 200:
            record = api_response.record
            record['street_line1'] = street_line1
            record['street_line2'] = street_line2
            record['town'] = town
            record['county'] = county
            record['postcode'] = postcode
            NannyGatewayActions().put('applicant-home-address', params=record)

        # create the address record if it didn't exist
        elif api_response.status_code == 404:
            apd_response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': app_id})
            if apd_response.status_code == 200:
                pd_id = apd_response.record['personal_detail_id']
                NannyGatewayActions().create(
                    'applicant-home-address',
                    params={
                        'application_id': app_id,
                        'personal_detail_id': pd_id,
                        'street_line1': street_line1,
                        'street_line2': street_line2,
                        'town': town,
                        'county': county,
                        'postcode': postcode,
                    }
                )

        return super().form_valid(form)


class PersonalDetailSummaryAddressView(NannyTemplateView):
    template_name = 'address-details.html'
    success_url_name = 'personal-details:Personal-Details-Lived-Abroad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
        if api_response.status_code == 200:
            context['address'] = AddressHelper.format_address(api_response.record, ", ")
        context['id'] = app_id
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle post requests to the guidance page.
        """
        app_id = app_id_finder(request)
        return HttpResponseRedirect(reverse('personal-details:Personal-Details-Lived-Abroad') + "?id=" + app_id)
