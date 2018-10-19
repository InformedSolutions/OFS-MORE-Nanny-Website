import datetime
from ..utils import get_form
from your_children_app.forms.your_children_details_form import YourChildrenDetailsForm
from django.http import HttpResponseRedirect
from nanny.utilities import build_url, app_id_finder
from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView


class YourChildrenDetailsView(NannyTemplateView):
    """
    Template view to  render the your children details view
    """
    template_name = "your-children-details.html"
    form_class = YourChildrenDetailsForm
    success_url_name = 'your-children:Your-Children-addresses'

    def get_initial(self):
        """
        Get initial defines the initial data for the form instance that is to be rendered on the page
        :return: a dictionary mapping form field names to values of the correct type
        """
        initial = super().get_initial()
        application_id = app_id_finder(self.request)
        response = NannyGatewayActions().read('applicant_children_details', params={'application_id': application_id})

        # Return existing record if one exists
        if response.status_code == 200:
            children_details_record = response.record
        elif response.status_code == 404:
            return initial

        initial['first_name'] = children_details_record['first_name']
        initial['middle_name'] = children_details_record['middle_name']
        initial['last_name'] = children_details_record['last_name']

        try:
            initial['date_of_birth'] = datetime.datetime.strptime(children_details_record['date_of_birth'], '%Y-%m-%d')
        except TypeError:
            initial['date_of_birth'] = None

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        application_id = app_id_finder(self.request)
        context['id'] = application_id
        application_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
        context['your_children_status'] = application_record['your_children_status']

        context['form'] = self.form_class
        context['fields'] = [context['form'].render_field(name, field) for name, field in context['form'].fields.items()]

        return context

    def form_valid(self, form):
        application_id = app_id_finder(self.request)
        child_id = self.request.GET['child_id'] if 'child_id' in self.request.GET else None

        data_dict = {
            'application_id':application_id,
            'child_id': child_id,
            'first_name':form.cleaned_data['first_name'],
            'middle_names':form.cleaned_data['middle_names'],
            'last_name':form.cleaned_data['last_name'],
            'date_of_birth':form.cleaned_data['date_of_birth'],
        }

        response = NannyGatewayActions().read('applicant_children_details', params={'application_id': application_id})
        if response.status_code == 200:
            NannyGatewayActions().patch('applicant_children_details', params=data_dict)
        elif response.status_code == 404:
            NannyGatewayActions().create('applicant_children_details', params=data_dict)

        return super().form_valid(form)




    """
    Need functionality for the 'add' and 'remove' children features, also how the form will be rendered 
    within the page!
    """

