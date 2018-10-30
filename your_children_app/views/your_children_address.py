from django.http import HttpResponseRedirect
from django.shortcuts import render
from nanny import NannyGatewayActions, reverse
from nanny.base_views import NannyFormView
from your_children_app import address_helper
from your_children_app.forms.your_children_address import YourChildrenPostcodeForm, YourChildrenAddressSelectionForm, \
    YourChildrenManualAddressForm


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
        form = YourChildrenPostcodeForm(id=application_id, child=child)
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

        return render(request, 'your-children-postcode.html', variables)

    def post(self, request, *args, **kwargs):
        """
        Method to handle post requests from the 'Your Children' postcode lookup page
        """
        application_id = request.POST["id"]
        child = request.POST["child"]
        form = YourChildrenPostcodeForm(id=application_id, child=child)
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

                return render(request, 'your-children-address-selection.html', variables)


class YourChildrenAddressSelectionView(NannyFormView):
    """
    Template view to  render the your children address selection view
    """

    def get(self, request, *args, **kwargs):
        """
        Method to handle get requests to the 'your children' postcode results and address selection view
        """
        application_id = request.GET["id"]
        child = request.GET["child"]

        application = NannyGatewayActions().read('application', params={'application_id': application_id})
        child_record = NannyGatewayActions().list('your-children', params={
            'application_id': application_id,
            'child': str(child),
        }).record[0]

        postcode = child_record['postcode']
        name = child_record['first_name'] + " " + child_record['last_name']
        addresses = address_helper.AddressHelper.create_address_lookup_list(postcode)

        if len(addresses) != 0:
            form = YourChildrenAddressSelectionForm(id=application_id, choices=addresses)

            if application['application_status'] == 'FURTHER_INFORMATION':
                form.error_summary_template_name = 'returned-error-summary.html'
                form.error_summary_title = 'There was a problem'

            variables = {
                'form': form,
                'application_id': application_id,
                'postcode': postcode,
                'name': name,
                'child': child,
            }

            return render(request, 'your-children-address-selection.html', variables)

        else:
            form = YourChildrenAddressSelectionForm(id=application_id, child=child)

            if application['application_status'] == 'FURTHER_INFORMATION':
                form.error_summary_template_name = 'returned-error-summary.html'
                form.error_summary_title = 'There was a problem'

            variables = {
                'form': form,
                'application_id': application_id,
                'child': child,
            }

            return render(request, 'your-children-address-selection.html', variables)

    def post(self, request, *args, **kwargs):
        """
        Method to handle post requests to the 'Your children' address selection page
        """
        application_id = request.GET["id"]
        child = request.GET["child"]

        application = NannyGatewayActions().read('application', params={'application_id': application_id})
        child_record = NannyGatewayActions().list('your-children', params={
            'application_id': application_id,
            'child': str(child),
        }).record[0]

        postcode = child_record['postcode']
        name = child_record['first_name'] + " " + child_record['last_name']
        addresses = address_helper.AddressHelper.create_address_lookup_list(postcode)

        form = YourChildrenAddressSelectionForm(id=application_id, choices=addresses)

        if form.is_valid():
            selected_address_index = int(request.POST["address"])
            selected_address = address_helper.AddressHelper.get_posted_address(selected_address_index, postcode)
            child_record['street_line1'] = selected_address['line1']
            child_record['street_line2'] = selected_address['line2']
            child_record['town'] = selected_address['townOrCity']
            child_record['postcode'] = selected_address['postcode']
            child_record['country'] = 'United Kingdom'

            NannyGatewayActions().patch('your-children', params=child_record)

            if application['application_status'] != 'COMPLETED':
                application['application_status'] = 'IN_PROGRESS'

            # Remove ARC flag
            child_list = NannyGatewayActions().list('your-children', params={
                'application_id': application_id,
                'ordering': 'child'
            })

            next_child = [child for child in child_list if child['line1'] is not None][0]

            if next_child is None:
                # All children have addresses
                return HttpResponseRedirect(reverse('your-children:Your-Children-Summary')
                                            + '?id=' + application_id)
            else:
                return HttpResponseRedirect(reverse('your-children:Your-Children-Postcode')
                                            + '?id=' + application_id
                                            + '&child=' + str(next_child)
                                            )

        else:
            form.error_summary_title = 'There was a problem finding your address'

            if application['application_status'] == 'FURTHER_INFORMATION':
                form.error_summary_template_name = 'returned-error-summary.html'
                form.error_summary_title = 'There was a problem'

            variables = {
                'postcode': postcode,
                'form': form,
                'application_id': application_id,
                'child': child,
                'name': name,
            }

            return render(request, 'your-children-address-selection.html', variables)


class YourChildrenManualAddressView(NannyFormView):
    """
    Form view to  render the your children details view
    """

    def get(self, request, *args, **kwargs):
        """
        Method for handling get requests to the manual address entry page in the 'Your children' task
        """
        application_id = request.GET["id"]
        child = request.GET["child"]

        application = NannyGatewayActions().read('application', params={'application_id': application_id})
        child_record = NannyGatewayActions().list('your-children', params={
            'application_id': application_id,
            'child': str(child),
        }).record[0]
        name = child_record['first_name'] + " " + child_record['last_name']
        form = YourChildrenManualAddressForm(id=application_id, child=child)

        if application['application_status'] == 'FURTHER_INFORMATION':
            form.error_summary_template_name = 'returned-error-summary.html'
            form.error_summary_title = 'There was a problem'

        variables = {

            'form': form,
            'child': child,
            'name': name,
            'application_id': application_id,
        }

        return render(request, 'your-children-manual-address.html', variables)

    def post(self, request, *args, **kwargs):
        """
        Method for handling get requests from the manual address entry page within the 'your children' task
        """
        application_id = request.GET["id"]
        child = request.GET["child"]
        application = NannyGatewayActions().read('application', params={'application_id': application_id})
        child_record = NannyGatewayActions().list('your-children', params={
            'application_id': application_id,
            'child': str(child),
        }).record[0]
        name = child_record['first_name'] + " " + child_record['last_name']
        form = YourChildrenManualAddressForm(id=application_id, child=child)

        if form.is_valid():
            # Patch the existing child record
            child_record['street_line1'] = form.cleaned_data['street_line1']
            child_record['street_line2'] = form.cleaned_data['street_line2']
            child_record['town'] = form.cleaned_data['town']
            child_record['county'] = form.cleaned_data['county']
            child_record['postcode'] = form.cleaned_data['postcode']
            NannyGatewayActions().patch('your-children', params={child_record})

            if application['application_status'] != 'COMPLETED':
                application['application_status'] = 'IN_PROGRESS'

            child_list = NannyGatewayActions().list('your-children', params={
                'application_id': application_id,
                'ordering': 'child'
            })

            next_child = [child for child in child_list if child['line1'] is not None][0]

            if next_child is None:
                # All children have addresses
                return HttpResponseRedirect(reverse('your-children:Your-Children-Summary')
                                            + '?id=' + application_id)

            return HttpResponseRedirect(reverse('your-children:Your-Children-Postcode')
                                        + '?id=' + application_id
                                        + '&child=' + str(next_child)
                                        )

        else:
            form.error_summary_title = 'There was a problem finding your address'
            if application['application_status'] == 'FURTHER_INFORMATION':
                form.error_summary_template_name = 'returned-error-summary.html'
                form.error_summary_title = 'There was a problem'

            variables = {
                'form': form,
                'application_id': application_id,
                'child': child,
                'name': name,
            }
            return render(request, 'your-children-manual-address.html', variables)
