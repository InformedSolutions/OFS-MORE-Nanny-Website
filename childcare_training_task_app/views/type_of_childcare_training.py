from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView

from login_app.utils import build_url

from childcare_training_task_app.forms import TypeOfChildcareTrainingForm

from nanny_models.childcare_training import ChildcareTraining


class TypeOfChildcareTrainingFormView(FormView):
    """
    Class containing the methods for handling requests to the 'Type-Of-Childcare-Training' page.
    """
    template_name = 'type-of-childcare-training.html'
    form_class = TypeOfChildcareTrainingForm
    success_url = 'Childcare-Training-Summary'

    def form_valid(self, form):
        application_id = self.request.GET['id']
        nanny_api_response = ChildcareTraining.api.get_record(application_id=application_id)

        if nanny_api_response.status_code == 404:
            nanny_api_response = self.create_childcare_training_record()

        record = nanny_api_response.record
        childcare_training = form.cleaned_data['childcare_training']

        for option, option_text in TypeOfChildcareTrainingForm.options:
            if option in childcare_training:
                record[option] = True
            else:
                record[option] = False

        put_response = ChildcareTraining.api.put(record=record)

        if put_response.status_code == 200:
            return super(TypeOfChildcareTrainingFormView, self).form_valid(form)
        else:
            raise RuntimeError('The Nanny-Gateway API did not update the record as expected.')

    def get_initial(self):
        """
        Method to get initial data with which to populate the form.
        """
        application_id = self.request.GET['id']
        nanny_api_response = ChildcareTraining.api.get_record(application_id=application_id)
        if nanny_api_response.status_code == 404:
            return {}
        elif nanny_api_response.status_code == 200:
            kwargs = dict((option, nanny_api_response.record[option]) for option, option_text in TypeOfChildcareTrainingForm.options)
            return kwargs
        else:
            raise RuntimeError('The Nanny-Gateway API did not respond as expected.')

    def create_childcare_training_record(self):
        application_id = self.request.GET['id']
        ChildcareTraining.api.create(application_id=application_id, model_type=ChildcareTraining)
        return ChildcareTraining.api.get_record(application_id=application_id)

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
