from datetime import datetime

from django.http import HttpResponseRedirect

from childcare_address_app.utils import build_url
from nanny.db_gateways import NannyGatewayActions
from .base import BaseFormView
from ..forms.childcare_location import ChildcareLocationForm


class ChildcareLocationView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the childcare location page.
    """

    template_name = 'childcare-location.html'
    success_url = ''
    form_class = ChildcareLocationForm

    def get_initial(self):
        initial = super().get_initial()
        app_id = self.request.GET['id']
        api_response = NannyGatewayActions().read(
            'applicant-home-address',
            {'application_id': app_id},
        )
        if api_response.status_code == 200:
            record = api_response.record
            initial['both_work_and_home_address'] = record['childcare_address']
            initial['home_address_id'] = record['home_address_id']
            initial['id'] = app_id
        return initial

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['id'] = self.request.GET['id']
        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]

        return super(ChildcareLocationView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        # pull the applicant's home address from their personal details
        app_id = self.request.GET['id']

        both_work_and_home_address = None
        if form.cleaned_data['both_work_and_home_address'] == 'True':
            both_work_and_home_address = True
            self.success_url = 'Childcare-Address-Details'
        elif form.cleaned_data['both_work_and_home_address'] == 'False':
            both_work_and_home_address = False
            self.success_url = 'Childcare-Address-Postcode-Entry'

        childcare_address_changed_to_false = self.__check_childcare_address_changed_to_false(app_id, both_work_and_home_address)

        apd_api_response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': app_id})

        if apd_api_response.status_code == 200:
            personal_detail_id = apd_api_response.record['personal_detail_id']
            aha_api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})

            if aha_api_response.status_code == 200:

                home_address_record = aha_api_response.record
                home_address_record['childcare_address'] = both_work_and_home_address
                NannyGatewayActions().put('applicant-home-address', params=home_address_record)

                # add new childcare address
                if both_work_and_home_address:
                    NannyGatewayActions().create(
                        'childcare-address',
                        params={
                            'date_created': datetime.today(),
                            'application_id': app_id,
                            'street_line1': home_address_record['street_line1'],
                            'street_line2': home_address_record['street_line2'],
                            'town': home_address_record['town'],
                            'county': home_address_record['county'],
                            'country': home_address_record['country'],
                            'postcode': home_address_record['postcode'],
                        }
                    )

        if childcare_address_changed_to_false:
            # Delete all childcare addresses that are the same as the Applicant's home address.
            self.__delete_home_childcare_addresses(app_id)
            redirect_url = build_url('Childcare-Address-Postcode-Entry', get={'id': app_id, 'add': '1'})
            return HttpResponseRedirect(redirect_url)

        return super(ChildcareLocationView, self).form_valid(form)

    @staticmethod
    def __check_childcare_address_changed_to_false(app_id, cleaned_childcare_address):
        """
        Returns True if the childcare_address field for the applicant's home address was False and has been changed to
        True.
        :param app_id: Application id
        :param cleaned_childcare_address: Boolean of cleaned form data.
        :return: Boolean
        """
        if not cleaned_childcare_address:
            nanny_actions = NannyGatewayActions()
            applicant_home_address_record = nanny_actions.read('applicant-home-address',
                                                               params={'application_id': app_id}).record

            if applicant_home_address_record['childcare_address']:
                return True

        return False

    @staticmethod
    def __delete_home_childcare_addresses(app_id):
        """
        Deletes childcare addresses that are the same as the home childcare address in all address fields.
        :param app_id: Applicant's id
        :return: None
        """
        nanny_actions = NannyGatewayActions()

        home_address_record = nanny_actions.read('applicant-home-address', params={'application_id': app_id}).record

        home_address_filter = {
            'application_id': app_id,
            'street_line1': home_address_record['street_line1'] if home_address_record['street_line1'] else "",
            'street_line2': home_address_record['street_line2'] if home_address_record['street_line2'] else "",
            'town': home_address_record['town'] if home_address_record['town'] else "",
            'county': home_address_record['county'] if home_address_record['county'] else "",
            'country': home_address_record['country'] if home_address_record['country'] else "",
            'postcode': home_address_record['postcode'] if home_address_record['postcode'] else ""
        }

        home_childcare_address_list = nanny_actions.list('childcare-address', params=home_address_filter).record

        for address in home_childcare_address_list:
            nanny_actions.delete('childcare-address', params={'childcare_address_id': address['childcare_address_id']})
