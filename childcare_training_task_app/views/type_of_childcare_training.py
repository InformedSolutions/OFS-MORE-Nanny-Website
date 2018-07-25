from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import HttpResponseRedirect, reverse
from django.views.generic import FormView

from nanny.utilities import build_url

from childcare_training_task_app.forms import TypeOfChildcareTrainingForm

from nanny_gateway import NannyGatewayActions


class TypeOfChildcareTrainingFormView(FormView):
    """
    Class containing the methods for handling requests to the 'Type-Of-Childcare-Training' page.
    """
    template_name = 'type-of-childcare-training.html'
    form_class = TypeOfChildcareTrainingForm
    success_url = 'Childcare-Training-Summary'

    def form_valid(self, form):
        application_id = self.request.GET['id']

        try:
            record = NannyGatewayActions().read('childcare-training', params={'application_id': application_id})
        except Exception as e:
            if e.error.title == '404 Not Found':
                record = NannyGatewayActions().create('childcare-training', params={'application_id': application_id})
            else:
               raise e

        childcare_training = form.cleaned_data['childcare_training']

        for option, option_text in TypeOfChildcareTrainingForm.options:
            if option in childcare_training:
                record[option] = True
            else:
                record[option] = False

        NannyGatewayActions().patch('childcare-training', params=record)

        if record['no_training']:  # If they have selected only 'No training' (wouldn't pass validation otherwise)
            self.success_url = 'Childcare-Training-Course'

        return super(TypeOfChildcareTrainingFormView, self).form_valid(form)

    def get_initial(self):
        """
        Method to get initial data with which to populate the form.
        """
        application_id = self.request.GET['id']

        try:
            record = NannyGatewayActions().read('childcare-training', params={'application_id': application_id})
            kwargs = dict((option, record[option]) for option, option_text in TypeOfChildcareTrainingForm.options)
            return kwargs
        except Exception as e:
            if e.error.title == '404 Not Found':
                return {}
            else:
               raise e

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
