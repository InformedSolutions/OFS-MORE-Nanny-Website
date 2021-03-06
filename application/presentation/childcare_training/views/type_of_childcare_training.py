from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import HttpResponseRedirect, reverse

from application.presentation.base_views import NannyFormView
from application.services.db_gateways import NannyGatewayActions
from application.presentation.utilities import build_url

from ..forms import TypeOfChildcareTrainingForm


class TypeOfChildcareTrainingFormView(NannyFormView):
    """
    Class containing the methods for handling requests to the 'Type-Of-Childcare-Training' page.
    """
    template_name = 'type-of-childcare-training.html'
    form_class = TypeOfChildcareTrainingForm
    success_url = 'Childcare-Training-Certificate'

    def form_valid(self, form):
        application_id = self.request.GET['id']
        nanny_api_response = NannyGatewayActions().read('childcare-training', params={'application_id': application_id})

        if nanny_api_response.status_code == 404:
            nanny_api_response = self.create_childcare_training_record()

        record = nanny_api_response.record
        childcare_training = form.cleaned_data['childcare_training']

        for option, option_text in TypeOfChildcareTrainingForm.options:
            if option in childcare_training:
                record[option] = True
            else:
                record[option] = False

        put_response = NannyGatewayActions().put('childcare-training', params=record)

        if record['no_training']:  # If they have selected only 'No training' (wouldn't pass validation otherwise)
            self.success_url = 'Childcare-Training-Course'

        if put_response.status_code == 200:
            return super(TypeOfChildcareTrainingFormView, self).form_valid(form)
        else:
            if settings.DEBUG:
                raise RuntimeError('The Nanny-Gateway API did not update the record as expected.')
            else:
                HttpResponseRedirect(reverse('Service-Unavailable'))

    def get_initial(self):
        """
        Method to get initial data with which to populate the form.
        """
        application_id = self.request.GET['id']
        nanny_api_response = NannyGatewayActions().read('childcare-training', params={'application_id': application_id})
        if nanny_api_response.status_code == 404:
            return {}
        elif nanny_api_response.status_code == 200:
            kwargs = dict((option, nanny_api_response.record[option]) for option, option_text in TypeOfChildcareTrainingForm.options)
            return kwargs
        else:
            raise RuntimeError('The Nanny-Gateway API did not respond as expected.')

    def create_childcare_training_record(self):
        application_id = self.request.GET['id']
        return NannyGatewayActions().create('childcare-training', params={'application_id': application_id})

    def get_success_parameters(self):
        """
        Method to return a dictionary of parameters to be included as variables in the success url, e.g. application_id.
        """
        return {'id': self.request.GET['id']}

    def get_success_url(self):
        """
        Method to construct a url encoded with the necessary varaibles and navigate to it upone successful submission of
        a form.
        :return: a full url for the next page.
        """
        if self.success_url:
            # If not none, run the build url util function.
            return build_url(self.success_url, get=self.get_success_parameters())
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")

    def get_context_data(self, **kwargs):
        kwargs['id'] = self.request.GET['id']
        return super(TypeOfChildcareTrainingFormView, self).get_context_data(**kwargs)
