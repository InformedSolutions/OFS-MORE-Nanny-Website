from coreapi.exceptions import ErrorMessage

from .base import BaseFormView
from ..forms.childcare_location import ChildcareLocationForm
from datetime import datetime

from nanny_gateway import NannyGatewayActions


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

        try:
            apd_api_response_record = NannyGatewayActions().read('applicant-personal-details', params={'application_id': app_id})
            apd_api_response = 200
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                apd_api_response = 404
            else:
                raise e

        if apd_api_response == 200:
            personal_detail_id = apd_api_response_record['personal_detail_id']

            # current assumption is that the personal details task will have to be filled out before
            # the user can complete any other task
            home_address_record = NannyGatewayActions().read('applicant-home-address',
                                                             params={
                                                                 'application_id': app_id,
                                                                 'personal_detail_id': personal_detail_id,
                                                                 # 'current_address': 'True',
                                                             })

            if form.cleaned_data['home_address'] == 'True':
                # update home address
                NannyGatewayActions().create('childcare-address',
                                             params={
                                                 'application_id': app_id,
                                                 'date_created': str(datetime.today()),
                                                 'street_line1': home_address_record['street_line1'],
                                                 'street_line2': home_address_record['street_line2'],
                                                 'town': home_address_record['town'],
                                                 'county': home_address_record['county'],
                                                 'country': home_address_record['country'],
                                                 'postcode': home_address_record['postcode']
                                             })
                home_address_record['childcare_address'] = True

            elif form.cleaned_data['home_address'] == 'False':
                home_address_record['childcare_address'] = False

            NannyGatewayActions().patch('applicant-home-address', params=home_address_record)

        if form.cleaned_data['home_address'] == 'True':
            self.success_url = 'Childcare-Address-Details'

        elif form.cleaned_data['home_address'] == 'False':
            self.success_url = 'Childcare-Address-Postcode-Entry'

        return super(ChildcareLocationView, self).form_valid(form)


    def get_initial(self):
        initial = super().get_initial()
        app_id = self.request.GET['id']
        initial['id'] = app_id

        try:
            record = NannyGatewayActions().read('applicant-home-address', params={'application_id': app_id})
            initial['home_address'] = record['childcare_address']
            initial['home_address_id'] = record['home_address_id']
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                pass
            else:
                raise e

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
