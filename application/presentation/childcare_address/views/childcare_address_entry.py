import uuid
from datetime import datetime

import inflect
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .base import BaseFormView, BaseTemplateView
from application.services.address_helper import *
from ..forms.childcare_address import *
from ..utils import *


def get_address_number(app_id, add):
    """
    A function that uses the API to find the number of complete and incomplete childcare addresses within the postcode
    lookup page.
    :param app_id: The ID of the current applicant
    :param add: A flag that is appended to the URL should a user use the 'add another address' button on the address
                details page.
                *** This can be abused by using the 'add another' button, completing a second address, then using the
                    back button to return to the postcode lookup page
    :return: Return tuple of the address number and the ordinal string for adaptable html content
    """
    formatter = inflect.engine()
    api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})

    # API records do not exist while on the postcode lookup page for the first time so the ordinal needs to be defined
    # outside of the address number
    if api_response.status_code == 404:
        return '1', 'First'

    complete_addresses = [address for address in api_response.record if address['street_line1'] is not None]

    # catch first time journey users or those using the back button from the address lookup page on the first journey
    if len(complete_addresses) == 0:
        addr_num = 1
    else:
        addr_num = len(complete_addresses) + 1 if add else len(complete_addresses)

    return str(addr_num), formatter.number_to_words(formatter.ordinal(addr_num)).title()


class ChildcareAddressPostcodeView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address postcode page.
    """
    template_name = 'childcare-address-postcode.html'
    success_url = 'Childcare-Address-Lookup'
    form_class = ChildcareAddressForm

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        app_id = self.request.GET['id']
        add = self.request.GET.get('add')  # Returns none if 'add another' button is not used - User using back button
        kwargs['add'] = add
        childcare_address_id = self.request.GET[
            'childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
        self.initial = {
            'id': app_id
        }

        api_response = NannyGatewayActions().list('childcare-address',
                                                  params={'application_id': app_id})

        if api_response.status_code == 200:
            api_response.record = [address for address in api_response.record if address['street_line1'] is not None]

        if 'childcare_address_id' in self.request.GET:
            self.initial['childcare_address_id'] = childcare_address_id

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]
        kwargs['id'] = app_id
        kwargs['addr_num'], kwargs['ordinal'] = get_address_number(app_id, add)
        return super(ChildcareAddressPostcodeView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """
        Re-route the user if the postcode given is accurate.
        """
        app_id = self.request.GET['id']
        childcare_address_id = self.request.GET[
            'childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
        postcode = form.cleaned_data['postcode']
        add_another = self.request.GET.get('add')

        if childcare_address_id:
            # update postcode of address
            api_response = NannyGatewayActions().read('childcare-address',
                                                      params={'childcare_address_id': childcare_address_id})
            api_response.record['postcode'] = postcode
            NannyGatewayActions().put('childcare-address', params=api_response.record)  # Update entire record.

        else:
            api_response = NannyGatewayActions().create(
                'childcare-address',
                params={
                    'date_created': datetime.today(),
                    'application_id': app_id,
                    'childcare_address_id': uuid.uuid4(),
                    'postcode': postcode
                }
            )
            if api_response.status_code == 201:
                childcare_address_id = api_response.record['childcare_address_id']

        return HttpResponseRedirect(build_url('Childcare-Address-Lookup', get={
            'id': app_id,
            'childcare_address_id': childcare_address_id,
            'add': add_another
        }))


class ChildcareAddressLookupView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address lookup page.
    """
    template_name = 'childcare-address-lookup.html'
    success_url = 'Childcare-Address-Details'
    form_class = ChildcareAddressLookupForm

    def form_valid(self, form):
        """
        Re-route the user if the address selected is valid.
        """
        app_id = self.request.GET['id']
        childcare_address_id = self.request.GET[
            'childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
        selected_address_index = form.cleaned_data['address']

        if childcare_address_id:
            # update postcode of address
            api_response = NannyGatewayActions().read('childcare-address',
                                                      params={'childcare_address_id': childcare_address_id})
            record = api_response.record
            selected_address = AddressHelper.get_posted_address(selected_address_index, record['postcode'])
            record['street_line1'] = selected_address['line1']
            record['street_line2'] = selected_address['line2']
            record['town'] = selected_address['townOrCity']
            record['postcode'] = selected_address['postcode']
            record['home_address'] = False
            NannyGatewayActions().put('childcare-address', params=record)

        return HttpResponseRedirect(build_url('Childcare-Address-Details', get={
            'id': app_id
        }))

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        app_id = self.request.GET['id']
        childcare_address_id = self.request.GET[
            'childcare_address_id'] if 'childcare_address_id' in self.request.GET else None

        self.initial = {
            'id': app_id
        }
        kwargs['id'] = app_id
        kwargs['childcare_address_id'] = childcare_address_id

        api_response = NannyGatewayActions().list('childcare-address',
                                                  params={'application_id': app_id})

        add = self.request.GET.get('add')  # Returns none if 'add another' button is not used - User using back button
        kwargs['add'] = add

        if api_response.status_code == 200:
            api_response.record = [address for address in api_response.record if address['street_line1'] is not None]

        if childcare_address_id:
            api_response = NannyGatewayActions().read('childcare-address',
                                                      params={'childcare_address_id': childcare_address_id})
            postcode = api_response.record['postcode']
            kwargs['postcode'] = postcode
            addresses = AddressHelper.create_address_lookup_list(postcode)

            self.initial['choices'] = addresses

            kwargs['addr_num'], kwargs['ordinal'] = get_address_number(app_id, add)
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]

        return super(ChildcareAddressLookupView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for lookup form
        """
        self.get_context_data()
        form = self.get_form()

        # Clear incomplete addresses from the API record
        app_id = self.request.GET['id']
        api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
        if api_response.status_code == 200:
            api_response.record = [address for address in api_response.record if address['street_line1'] is not None]

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ChildcareAddressManualView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address manual entry page.
    """
    template_name = 'childcare-address-manual.html'
    success_url = 'Childcare-Address-Details'
    form_class = ChildcareAddressManualForm

    def form_valid(self, form):
        """
        Re-route the user if the manual address given is valid.
        """
        app_id = self.request.GET['id']
        childcare_address_id = self.request.GET[
            'childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
        street_line1 = form.cleaned_data['street_line1']
        street_line2 = form.cleaned_data['street_line2']
        town = form.cleaned_data['town']
        county = form.cleaned_data['county']
        postcode = form.cleaned_data['postcode']

        if childcare_address_id:
            # update postcode of address
            api_response = NannyGatewayActions().read('childcare-address',
                                                      params={'childcare_address_id': childcare_address_id})
            record = api_response.record
            record['street_line1'] = street_line1
            record['street_line2'] = street_line2
            record['town'] = town
            record['county'] = county
            record['postcode'] = postcode
            record['home_address'] = False
            NannyGatewayActions().patch('childcare-address', params=record)

        else:
            NannyGatewayActions().create(
                'childcare-address',
                params={
                    'date_created': datetime.today(),
                    'application_id': app_id,
                    'street_line1': street_line1,
                    'street_line2': street_line2,
                    'town': town,
                    'county': county,
                    'postcode': postcode,
                    'home_address': False
                }
            )

        #  Redefine API response so that incorrect address records can be removed
        api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
        incomplete_addresses = [address for address in api_response.record if address['street_line1'] is None]

        # Delete record that have not being completed - only invalid
        for address in incomplete_addresses:
            NannyGatewayActions().delete('childcare-address', params=address)

        return HttpResponseRedirect(build_url('Childcare-Address-Details', get={
            'id': app_id,
            'add': 0
        }))

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        app_id = self.request.GET['id']

        childcare_address_id = self.request.GET[
            'childcare_address_id'] if 'childcare_address_id' in self.request.GET else None

        add = self.request.GET.get('add')  # Returns none if 'add another' button is not used - User using back button

        self.initial = {
            'id': app_id
        }

        kwargs['id'] = app_id
        kwargs['add'] = add
        api_response = NannyGatewayActions().list('childcare-address',
                                                  params={'application_id': app_id})

        if api_response.status_code == 200:
            api_response.record = [address for address in api_response.record if address['street_line1'] is not None]

        if childcare_address_id:
            self.initial['childcare_address_id'] = childcare_address_id
            kwargs['childcare_address_id'] = childcare_address_id

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]
        kwargs['addr_num'], kwargs['ordinal'] = get_address_number(app_id, add)

        return super(ChildcareAddressManualView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for lookup form
        """
        self.get_context_data()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# TODO: Check field names how will flagging work here???
class ChildcareAddressDetailsView(BaseTemplateView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address details page.
    """
    template_name = 'childcare-address-details.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Method to redirect to Where you work page when the applicant removes all addresses
        :return: HTTP response redirect
        """

        app_id = self.request.GET['id']

        api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})

        # If the number of childcare addresses equal to 1 and the applicant clicks the Remove this address link
        if 'childcare-address-id' in self.request.GET:

            if api_response.status_code == 200 and len(api_response.record) <= 1:

                # Check if childcare address exists (to handle page reloads)
                childcare_address_id = self.request.GET['childcare-address-id']
                last_childcare_address = NannyGatewayActions().list('childcare-address',
                                                                    params={
                                                                        'childcare_address_id': childcare_address_id})

                if last_childcare_address.status_code == 200:

                    if len(last_childcare_address.record) > 0:
                        # Delete the childcare address
                        childcare_address_id = self.request.GET['childcare-address-id']
                        NannyGatewayActions().delete('childcare-address',
                                                     params={'childcare_address_id': childcare_address_id})

                        # Set Where you work default response to No
                        application_response = NannyGatewayActions().read('application',
                                                                          params={'application_id': app_id})

                        record = application_response.record
                        record['address_to_be_provided'] = False
                        NannyGatewayActions().put('application', params=record)

                        # set childcare location to false
                        ha_response =  NannyGatewayActions().read('applicant-home-address',
                                                                          params={'application_id': app_id})
                        if ha_response.status_code == 200:
                            ha_record = ha_response.record
                            ha_record['childcare_address'] = False
                            NannyGatewayActions().put('applicant-home-address', ha_record)


                        # Redirect to Where you work page
                        return HttpResponseRedirect(build_url('Childcare-Address-Where-You-Work', get={
                            'id': app_id,
                        }))

        return super(ChildcareAddressDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Override base BaseTemplateView method to add 'fields' key to context for rendering in template.
        """
        app_id = self.request.GET['id']
        kwargs['id'] = app_id

        #  Redefine API response so that incorrect address records can be removed
        api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
        if api_response.status_code == 200:
            incomplete_addresses = [address for address in api_response.record if address['street_line1'] is None]

            # Delete record that have not being completed
            for address in incomplete_addresses:
                NannyGatewayActions().delete('childcare-address', params=address)

        # If clicking on Remove this address link
        if 'childcare-address-id' in self.request.GET:
            childcare_address_id = self.request.GET['childcare-address-id']
            childcare_address_api_response = NannyGatewayActions().read('childcare-address', params = {'childcare_address_id': childcare_address_id})
            home_address_response = NannyGatewayActions().read('applicant-home-address', params = {'application_id': app_id})
            NannyGatewayActions().delete('childcare-address', params={'childcare_address_id': childcare_address_id})
            if childcare_address_api_response.status_code == 200 and home_address_response.status_code == 200:
                ca_record = childcare_address_api_response.record
                ha_record = home_address_response.record
                if ca_record['home_address'] == True:
                    ha_record['childcare_address'] = False
                    NannyGatewayActions().put('applicant-home-address', params=ha_record)

        # Generate list of childcare addresses and display in through page context
        api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})

        addresses = {}
        count = 1
        if api_response.status_code == 200:
            for address in api_response.record:
                addresses[str(count)] = {
                    "address": AddressHelper.format_address(address, ", "),
                    "childcare_address_id": address['childcare_address_id']
                }
                count += 1
        kwargs['childcare_addresses'] = sorted(addresses.items())

        return super(ChildcareAddressDetailsView, self).get_context_data(**kwargs)

    def post(self, request):
        """
        Handle post requests to the details page.
        """
        app_id = request.GET['id']
        if 'add_another' in request.POST:
            api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
            if api_response.status_code == 200 and len(api_response.record) > 4:
                context = self.get_context_data()
                context['non_field_errors'] = ["You can only enter up to 5 childcare addresses"]
                context['error_summary_title'] = "There was a problem"
                return render(request, self.template_name, context)

            # Return the URL with a flag that is used to increment the number of addresses
            return HttpResponseRedirect(build_url('Childcare-Address-Postcode-Entry', get={
                'id': app_id,
                'add': 1
            }))
        else:
            return HttpResponseRedirect(build_url('Childcare-Address-Summary', get={
                'id': app_id,
            }))
