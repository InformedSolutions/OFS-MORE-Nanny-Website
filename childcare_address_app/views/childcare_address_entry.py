import uuid
from .base import BaseFormView, BaseTemplateView
from ..forms.childcare_address import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..utils import *
from ..address_helper import *
import inflect
from datetime import datetime

from nanny.db_gateways import NannyGatewayActions


def get_address_number_postcode(app_id, add, ord):
    """

    :param app_id:
    :param add:
    :param ord:
    :return:
    """
    formatter = inflect.engine()
    api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})

    if api_response.status_code == 404:
        return 'First'

    complete_addresses = [address for address in api_response.record if address['street_line1'] is not None]

    if len(complete_addresses) == 0:
        addr_num = 1
    else:
        if add:
            addr_num = len(complete_addresses) + 1
        else:
            addr_num = len(complete_addresses)

    if ord:
        return formatter.number_to_words(formatter.ordinal(addr_num)).title()
    else:
        return str(addr_num)


def get_address_number_address_lookup(app_id, add, ord):
    """

    :param app_id:
    :param add:
    :param ord:
    :return:
    """
    formatter = inflect.engine()
    api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
    complete_addresses = [address for address in api_response.record if address['street_line1'] is not None]
    incomplete_addresses = [address for address in api_response.record if address['street_line1'] is None]

    if len(incomplete_addresses) > 0:
        if add != 'None':
            addr_num = len(complete_addresses) + 1
        else:
            addr_num = len(complete_addresses)
    else:
        addr_num = len(complete_addresses)

    if ord:
        return formatter.number_to_words(formatter.ordinal(addr_num)).title()
    else:
        return str(addr_num)


# def get_address_number_postcode(app_id, add, ord):
#     """
#     get ordinal value of this childcare address
#     :param app_id: id of the application
#     :return:
#     """
#     formatter = inflect.engine()
#     api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
#
#     # If no record exists set ordinal to First
#     if api_response.status_code == 404:
#         return 'First'
#     else:
#         api_response.record = [address for address in api_response.record if address['street_line1'] is not None]
#         index = len(api_response.record)
#
#         if add or len(api_response.record) == 0:
#             #  If the user has entered this page through the use of the 'add another address' button, increase the
#             #  index number for correct ordinals and address number displayed within the html
#             index += 1
#
#         if ord:
#             return formatter.number_to_words(formatter.ordinal(index)).title()
#         else:
#             return str(index)
#

# def get_address_number_address_lookup(app_id, ord):
#     """
#
#     :param app_id:
#     :param ord:
#     :return:
#     """
#     formatter = inflect.engine()
#     api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
#     complete_addresses = [address for address in api_response.record if address['street_line1'] is not None]
#     incomplete_addresses = [address for address in api_response.record if address['street_line1'] is None]
#
#     # Catch users coming back from the address details page
#     if len(incomplete_addresses) == 0:
#         index = len(complete_addresses)
#     else:
#         index = len(complete_addresses) + 1
#     if ord:
#         return formatter.number_to_words(formatter.ordinal(index)).title()
#     else:
#         return str(index)


class ChildcareAddressPostcodeView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address postcode page.
    """
    template_name = 'childcare-address-postcode.html'
    success_url = 'Childcare-Address-Lookup'
    form_class = ChildcareAddressForm

    def form_valid(self, form):
        """
        Re-route the user if the postcode given is accurate.
        """
        app_id = self.request.GET['id']
        childcare_address_id = self.request.GET['childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
        postcode = form.cleaned_data['postcode']
        add_another = self.request.GET.get('add')

        if childcare_address_id:
            # update postcode of address
            api_response = NannyGatewayActions().read('childcare-address', params={'childcare_address_id': childcare_address_id})
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

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        app_id = self.request.GET['id']
        add = self.request.GET.get('add')  # Returns none if 'add another' button is not used - User using back button
        childcare_address_id = self.request.GET['childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
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

        kwargs['ordinal'] = get_address_number_postcode(app_id, add, True)
        kwargs['addr_num'] = get_address_number_postcode(app_id, add, False)

        return super(ChildcareAddressPostcodeView, self).get_context_data(**kwargs)


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
        childcare_address_id = self.request.GET['childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
        selected_address_index = form.cleaned_data['address']

        if childcare_address_id:
            # update postcode of address
            api_response = NannyGatewayActions().read('childcare-address', params={'childcare_address_id': childcare_address_id})
            record = api_response.record
            selected_address = AddressHelper.get_posted_address(selected_address_index, record['postcode'])
            record['street_line1'] = selected_address['line1']
            record['street_line2'] = selected_address['line2']
            record['town'] = selected_address['townOrCity']
            record['postcode'] = selected_address['postcode']
            NannyGatewayActions().put('childcare-address', params=record)

        #  Redefine API response so that incorrect address records can be removed
        api_response = NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
        incomplete_addresses = [address for address in api_response.record if address['street_line1'] is None]

        # Delete record that have not being completed - only invalid
        for address in incomplete_addresses:
            NannyGatewayActions().delete('childcare-address', params=address)

        return HttpResponseRedirect(build_url('Childcare-Address-Details', get={
            'id': app_id,
            }))

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        app_id = self.request.GET['id']
        childcare_address_id = self.request.GET['childcare_address_id'] if 'childcare_address_id' in self.request.GET else None

        self.initial = {
            'id': app_id
        }
        kwargs['id'] = app_id
        kwargs['childcare_address_id'] = childcare_address_id

        api_response = NannyGatewayActions().list('childcare-address',
                                                  params={'application_id': app_id})

        add = self.request.GET.get('add')  # Returns none if 'add another' button is not used - User using back button

        if api_response.status_code == 200:
            api_response.record = [address for address in api_response.record if address['street_line1'] is not None]

        if childcare_address_id:
            api_response = NannyGatewayActions().read('childcare-address',
                                                      params={'childcare_address_id': childcare_address_id})
            postcode = api_response.record['postcode']
            kwargs['postcode'] = postcode
            addresses = AddressHelper.create_address_lookup_list(postcode)

            self.initial['choices'] = addresses

            kwargs['ordinal'] = get_address_number_address_lookup(app_id, add, True)
            kwargs['addr_num'] = get_address_number_address_lookup(app_id, add, False)

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
        childcare_address_id = self.request.GET['childcare_address_id'] if 'childcare_address_id' in self.request.GET else None
        add = self.request.GET.get('add')  # Returns none if 'add another' button is not used - User using back button

        self.initial = {
            'id': app_id
        }
        
        kwargs['id'] = app_id

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

        kwargs['ordinal'] = get_address_number_address_lookup(app_id, add, True)
        kwargs['addr_num'] = get_address_number_address_lookup(app_id, add, False)

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


class ChildcareAddressDetailsView(BaseTemplateView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address details page.
    """
    template_name = 'childcare-address-details.html'

    def get_context_data(self, **kwargs):
        """
        Override base BaseTemplateView method to add 'fields' key to context for rendering in template.
        """
        app_id = self.request.GET['id']
        kwargs['id'] = app_id
        api_response = NannyGatewayActions().list('childcare-address',
                                                  params={'application_id': app_id})

        if api_response.status_code == 200:
            api_response.record = [address for address in api_response.record if address['street_line1'] is not None]

        addresses = {}
        count = 1
        if api_response.status_code == 200:
            for address in api_response.record:
                addresses[str(count)] = AddressHelper.format_address(address, ", ")
                count += 1
        kwargs['childcare_addresses'] = sorted(addresses.items())

        return super(ChildcareAddressDetailsView, self).get_context_data(**kwargs)

    def post(self, request):
        """
        Handle post requests to the details page.
        """
        app_id = request.GET['id']
        if 'add_another' in request.POST:
            api_response = NannyGatewayActions().list('childcare-address',
                                                  params={'application_id': app_id})
            if api_response.status_code == 200 and len(api_response.record) > 4:
                context = self.get_context_data()
                context['non_field_errors'] = ["You can only enter up to 5 childcare addresses"]
                context['error_summary_title'] = "There was a problem"
                return render(request, self.template_name, context)
            return HttpResponseRedirect(build_url('Childcare-Address-Postcode-Entry', get={
                'id': app_id,
                'add': 1
                }))
        else:
            return HttpResponseRedirect(build_url('Childcare-Address-Summary', get={
                'id': app_id,
                }))
