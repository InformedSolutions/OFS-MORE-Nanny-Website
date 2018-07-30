from .base import BaseFormView
from ..forms.childcare_location import ChildcareLocationForm
from datetime import datetime

from nanny.db_gateways import NannyGatewayActions


class ChildcareLocationView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the childcare location page.
    """

    template_name = 'childcare-location.html'
    success_url = ''
    form_class = ChildcareLocationForm

    def form_valid(self, form):
        # pull the applicant's home address from their personal details
        app_id = self.request.GET['id']

        home_address = None
        if form.cleaned_data['home_address'] == 'True':
            home_address = True
            self.success_url = 'Childcare-Address-Details'
        elif form.cleaned_data['home_address'] == 'False':
            home_address = False
            self.success_url = 'Childcare-Address-Postcode-Entry'

        apd_api_response = NannyGatewayActions().read('applicant-personal-details', params={'application_id': app_id})

        if apd_api_response.status_code == 200:
            personal_detail_id = apd_api_response.record['personal_detail_id']
            aha_api_response = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})

            if aha_api_response.status_code == 200:

                home_address_record = aha_api_response.record
                home_address_record['childcare_address'] = home_address
                NannyGatewayActions().put('applicant-home-address', params=home_address_record)

                # add new childcare address
                if home_address:
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

            # if applicant home address has not been created, do so for purposes of storing childcare location
            else:
                NannyGatewayActions().create(
                    'applicant-home-address',
                    params={
                        'application_id': app_id,
                        'personal_detail_id': personal_detail_id,
                        'childcare_location': home_address,
                    }
                )

        # if personal details has not been created, do so for purposes of storing childcare location
        else:
            apd_api_response_create = NannyGatewayActions().create(
                'applicant-personal-details',
                {'application_id': app_id},
            )
            if apd_api_response_create.status_code == 201:
                record = apd_api_response_create.record
                NannyGatewayActions().create(
                    'applicant-home-address',
                    params={
                        'application_id': app_id,
                        'personal_detail_id': record['personal_detail_id'],
                        'childcare_location': home_address,
                    }
                )

        return super(ChildcareLocationView, self).form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        app_id = self.request.GET['id']
        api_response = NannyGatewayActions().read(
                'applicant-home-address',
                {'application_id': app_id},
            )
        if api_response.status_code == 200:
            record = api_response.record
            initial['home_address'] = record['childcare_address']
            initial['home_address_id'] = record['home_address_id']
            initial['id'] = app_id
        return initial

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]

        kwargs['id'] = self.request.GET['id']

        return super(ChildcareLocationView, self).get_context_data(**kwargs)
