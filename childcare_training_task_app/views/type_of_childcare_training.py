from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView

from login_app.utils import build_url

from childcare_training_task_app.forms import TypeOfChildcareTrainingForm

# from nanny_models.application import ChildcareTraining


class TypeOfChildcareTrainingFormView(FormView):
    """
    Class containing the methods for handling requests to the 'Type-Of-Childcare-Training' page.
    """
    template_name = 'type-of-childcare-training.html'
    form_class = TypeOfChildcareTrainingForm
    success_url = 'Childcare-Training-Summary'

    def form_valid(self, form):
        # TODO: Update values in ChildcareTraining model in Nanny-Gateway.
        return super(TypeOfChildcareTrainingFormView, self).form_valid(form)

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
            # If not none, run the build url util function
            return build_url(self.success_url, get=self.get_success_parameters())
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
