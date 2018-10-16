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


class YourChildrenView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the childcare address postcode page.
    """
    template_name = 'your_children_details.html'
    success_url = # TODO - Add this and import the form once it is added to the init/form
    form_class = YourChildrenDetailsForm

    def form_valid(self, form):
        """
        Re-route the user if the child details given pass validation
        """
        app_id = self.request.GET['id']
        child_id = self.request.GET[
            'child_id'] if 'child_id' in self.request.GET else None

        child_first_name = form.cleaned_data['child_first_name']
        child_middle_name = form.cleaned_data['child_middle_name']
        child_last_name = form.cleaned_data['child_last_name']
        child_dob = form.cleaned_data['child_dob']

        if child_id:
            # update child details
            api_response = NannyGatewayActions().read('child_id', params={'child_id': child_id})
            api_response.record['child_first_name'] = child_first_name
            api_response.record['child_middle_name'] = child_middle_name
            api_response.record['child_last_name'] = child_last_name
            api_response.record['child_dob'] = child_dob
            NannyGatewayActions().put('child_id', params=api_response.record)  # Update entire record.

        else:
            # Create a new record for each child
            api_response = NannyGatewayActions().create(
                'own_child',
                params={
                    'date_created': datetime.today(),
                    'application_id': app_id,
                    'child_id': uuid.uuid4(),
                    'child_first_name': child_first_name,
                    'child_middle_name': child_middle_name,
                    'child_last_name': child_last_name,
                    'child_dob': child_dob,
                }
            )
            if api_response.status_code == 201:
                childcare_address_id = api_response.record['childcare_address_id']

        return HttpResponseRedirect(build_url('Childcare-Address-Lookup', get={
            'id': app_id,
            'childcare_address_id': childcare_address_id
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

        if 'childcare_address_id' in self.request.GET:
            self.initial['childcare_address_id'] = childcare_address_id

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]
        kwargs['id'] = app_id

        kwargs['ordinal'] = get_address_number(app_id, childcare_address_id, True)
        kwargs['addr_num'] = get_address_number(app_id, childcare_address_id, False)

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

        if childcare_address_id:
            api_response = NannyGatewayActions().read('childcare-address',
                                                      params={'childcare_address_id': childcare_address_id})
            postcode = api_response.record['postcode']
            kwargs['postcode'] = postcode
            addresses = AddressHelper.create_address_lookup_list(postcode)

            self.initial['choices'] = addresses

            kwargs['ordinal'] = get_address_number(app_id, childcare_address_id, True)
            kwargs['addr_num'] = get_address_number(app_id, childcare_address_id, False)

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

        if childcare_address_id:
            self.initial['childcare_address_id'] = childcare_address_id
            kwargs['childcare_address_id'] = childcare_address_id

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]

        kwargs['ordinal'] = get_address_number(app_id, childcare_address_id, True)
        kwargs['addr_num'] = get_address_number(app_id, childcare_address_id, False)

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

                # Delete the childcare address
                childcare_address_id = self.request.GET['childcare-address-id']
                NannyGatewayActions().delete('childcare-address', params={'childcare_address_id': childcare_address_id})

                # Set Where you work default response to No
                application_response = NannyGatewayActions().read('application', params={'application_id': app_id})
                record = application_response.record
                record['address_to_be_provided'] = False
                NannyGatewayActions().put('application', params=record)

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

        # If clicking on Remove this address link
        if 'childcare-address-id' in self.request.GET:
            childcare_address_id = self.request.GET['childcare-address-id']
            NannyGatewayActions().delete('childcare-address', params={'childcare_address_id': childcare_address_id})

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
            return HttpResponseRedirect(build_url('Childcare-Address-Postcode-Entry', get={
                'id': app_id,
            }))
        else:
            return HttpResponseRedirect(build_url('Childcare-Address-Summary', get={
                'id': app_id,
            }))
