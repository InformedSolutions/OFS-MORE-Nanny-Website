from .BASE import *
from ..forms.home_address import HomeAddressForm, HomeAddressLookupForm, HomeAddressManualForm
from ..utils import app_id_finder, build_url
from ..address_helper import *
from django.http import HttpResponseRedirect
from django.urls import reverse

from nanny_models.applicant_home_address import *
from nanny_models.applicant_personal_details import *


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

        api_response = ApplicantHomeAddress.api.get_record(application_id=application_id)
        if api_response.status_code == 200:
            address_record = api_response.record
            address_record['postcode'] = postcode
            ApplicantHomeAddress.api.put(address_record)
        else:
            personal_details = ApplicantPersonalDetails.api.get_record(application_id=application_id).record
            ApplicantHomeAddress.api.create(
                application_id=application_id,
                personal_detail_id=personal_details['personal_detail_id'],
                postcode=postcode,
                model_type=ApplicantHomeAddress
            )

        return super().form_valid(form)


class PersonalDetailSelectAddressView(BaseFormView):

    template_name = 'personal-details-home-address-lookup.html'
    form_class = HomeAddressLookupForm
    success_url = 'personal-details:Personal-Details-Address-Summary'

    def form_valid(self, form):
        app_id = app_id_finder(self.request)
        selected_address_index = form.cleaned_data['address']
        api_response = ApplicantHomeAddress.api.get_record(application_id=app_id)
        if api_response.status_code == 200:
            record = api_response.record
            selected_address = AddressHelper.get_posted_address(selected_address_index, record['postcode'])
            record['street_line1'] = selected_address['line1']
            record['street_line2'] = selected_address['line2']
            record['town'] = selected_address['townOrCity']
            record['county'] = None
            record['postcode'] = selected_address['postcode']
            ApplicantHomeAddress.api.put(record)  # Update entire record.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)

        context['id'] = app_id

        api_response = ApplicantHomeAddress.api.get_record(application_id=app_id)
        if api_response.status_code == 200:
            postcode = api_response.record['postcode']
            context['postcode'] = postcode
            self.initial['choices'] = AddressHelper.create_address_lookup_list(postcode)

        return context


class PersonalDetailManualAddressView(BaseFormView):

    template_name = 'personal-details-home-address-manual.html'
    success_url = 'personal-details:Personal-Details-Address-Summary'
    form_class = HomeAddressManualForm

    def get_initial(self):
        initial = super().get_initial()
        app_id = app_id_finder(self.request)

        api_response = ApplicantHomeAddress.api.get_record(application_id=app_id)
        if api_response.status_code == 200:
            initial['street_line1'] = api_response.record['street_line1']
            initial['street_line2'] = api_response.record['street_line2']
            initial['town'] = api_response.record['town']
            initial['county'] = api_response.record['county']
            initial['postcode'] = api_response.record['postcode']

        self.initial['choices'] = AddressHelper.create_address_lookup_list(api_response.record['postcode'])
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)

        context['id'] = app_id

        return context


class PersonalDetailSummaryAddressView(BaseTemplateView):

    template_name = 'address-details.html'
    success_url = 'personal-details:Personal-Details-Lived-Abroad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        app_id = app_id_finder(self.request)
        api_response = ApplicantHomeAddress.api.get_record(application_id=app_id)
        if api_response.status_code == 200:
            context['address'] = AddressHelper.format_address(api_response.record, ", ")
        context['id'] = app_id
        return context

    def post(self, request):
        """
        Handle post requests to the guidance page.
        """
        app_id = app_id_finder(self.request)
        return HttpResponseRedirect(reverse('personal-details:Personal-Details-Lived-Abroad') + "?id=" + app_id)
