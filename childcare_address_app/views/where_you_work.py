from nanny import NannyFormView
from nanny.db_gateways import NannyGatewayActions
from ..forms.where_you_work import WhereYouWorkForm


class WhereYouWorkView(NannyFormView):
    """
    Class containing the view(s) for handling the GET requests to the where you work page.
    """

    template_name = 'where-you-work.html'
    success_url = ''
    form_class = WhereYouWorkForm

    def form_valid(self, form):
        app_id = self.request.GET.get('id')
        nanny_actions = NannyGatewayActions()
        address_to_be_provided = form.cleaned_data['address_to_be_provided']

        # Convert address_to_be_provided to a boolean.
        address_to_be_provided = address_to_be_provided == 'True' \
            if type(address_to_be_provided) == str \
            else address_to_be_provided

        application_record = nanny_actions.read('application', params={'application_id': app_id}).record

        # Patch new address_to_be_provided value
        patch_record = {
            'application_id': application_record['application_id'],
            'address_to_be_provided': address_to_be_provided,
            'childcare_address_status': 'IN_PROGRESS'
        }
        nanny_actions.patch('application', params=patch_record)

        # Set success_url
        if address_to_be_provided:
            self.success_url = 'Childcare-Address-Location'
        else:
            self.success_url = 'Childcare-Address-Details-Later'

            # Delete all existing childcare addresses, if any exist.
            self.__delete_childcare_addresses(app_id)

            # Nullify answer to 'Will you work and live at the same address?'
            self.__nullify_answers(app_id)

        return super(WhereYouWorkView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Override base BaseFormView method to add 'fields' key to context for rendering in template.
        """
        self.initial = {
            'id': self.request.GET['id']
        }

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]
        kwargs['id'] = self.request.GET['id']

        return super(WhereYouWorkView, self).get_context_data(**kwargs)

    @staticmethod
    def __delete_childcare_addresses(app_id):
        nanny_actions = NannyGatewayActions()

        childcare_address_list_response = nanny_actions.list('childcare-address', params={'application_id': app_id})

        if childcare_address_list_response.status_code == 200:
            childcare_address_list_record = childcare_address_list_response.record

            for childcare_address in childcare_address_list_record:
                nanny_actions.delete('childcare-address',
                                     params={'childcare_address_id': childcare_address['childcare_address_id']})

    @staticmethod
    def __nullify_answers(app_id):
        """
        Function to nullify any relevant workflow answers.
        :param app_id: Applicant's id
        :return: None
        """
        nanny_actions = NannyGatewayActions()

        # Nullify answer to 'Will you work and live at the same address?'
        applicant_home_address_response = NannyGatewayActions().read('applicant-home-address',
                                                                     params={'application_id': app_id})

        if applicant_home_address_response.status_code == 200:
            put_record = applicant_home_address_response.record
            put_record['childcare_address'] = 'null'

            nanny_actions.put('applicant-home-address', params=put_record)
