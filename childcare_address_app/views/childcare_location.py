from .base import BaseFormView
from ..forms.childcare_location import ChildcareLocationForm
from datetime import datetime
from nanny_models.applicant_home_address import *
from nanny_models.childcare_address import *


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
        apd_api_response = ApplicantPersonalDetails.api.get_record(application_id=app_id)
        if apd_api_response.status_code == 200:
            personal_detail_id = apd_api_response.record['personal_detail_id']
            aha_api_response = ApplicantHomeAddress.api.get_record(
                personal_detail_id=personal_detail_id,
                current_address=True
            )

            if aha_api_response.status_code == 200:

                # current assumption is that the personal details task will have to be filled out before
                # the user can complete any other task
                home_address_record = aha_api_response.record

                # update home address
                if form.cleaned_data['home_address'] == 'True':

                    ChildcareAddress.api.create(
                        model_type=ChildcareAddress,
                        application_id=app_id,
                        date_created=datetime.today(),
                        street_line1=home_address_record['street_line1'],
                        street_line2=home_address_record['street_line2'],
                        town=home_address_record['town'],
                        county=home_address_record['county'],
                        country=home_address_record['country'],
                        postcode=home_address_record['postcode']
                    )
                    home_address_record['childcare_address'] = True

                elif form.cleaned_data['home_address'] == 'False':
                    home_address_record['childcare_address'] = False

                ApplicantHomeAddress.api.put(home_address_record)

        if form.cleaned_data['home_address'] == 'True':
            self.success_url = 'Childcare-Address-Details'

        elif form.cleaned_data['home_address'] == 'False':
            self.success_url = 'Childcare-Address-Postcode-Entry'

        return super(ChildcareLocationView, self).form_valid(form)


    def get_initial(self):
        initial = super().get_initial()
        app_id = self.request.GET['id']
        api_response = ApplicantHomeAddress.api.get_record(application_id=app_id)
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
