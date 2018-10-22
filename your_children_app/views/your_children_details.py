from your_children_app.forms.your_children_details_form import YourChildrenDetailsForm
from nanny.utilities import build_url, app_id_finder
from nanny.base_views import NannyTemplateView
import uuid
from ..utils import *
from nanny.db_gateways import NannyGatewayActions


class YourChildrenDetailsView(FormMixin, NannyTemplateView):
    """
    Template view to  render the your children details view
    """
    template_name = "your-children-details.html"
    form_class = YourChildrenDetailsForm
    success_url_name = 'your-children:Your-Children-addresses'

    def form_valid(self, form):
        application_id = app_id_finder(self.request)
        child_id = self.request.GET['child_id'] if 'child_id' in self.request.GET else None

        first_name = form.cleaned_data['first_name']
        middle_names = form.cleaned_data['middle_names']
        last_name = form.cleaned_data['last_name']
        date_of_birth = form.cleaned_data['date_of_birth']

        if child_id:
            # Update an existing child's record
            api_response = NannyGatewayActions().read('your-children', params={'child_id': child_id})

            api_response.record['first_name'] = first_name
            api_response.record['middle_names'] = middle_names
            api_response.record['last_name'] = last_name
            api_response.record['date_of_birth'] = date_of_birth

            NannyGatewayActions().put('your-children', params=api_response.record)

        else:
            api_response = NannyGatewayActions().create(
                'your-children',
                params={
                    'application_id': application_id,
                    'child_id': uuid.uuid4(),
                    'first_name': first_name,
                    'middle_names': middle_names,
                    'last_name': last_name,
                    'date_of_birth': date_of_birth,
                }
            )

            if api_response.status_code == 201:
                child_id = api_response.record['child_id']

        return HttpResponseRedirect(build_url(
            'your-children:Your-Children-addresses',
            get={
                'id': application_id,
                'child_id': child_id,
            }
        ))

    def get_context_data(self, **kwargs):

        application_id = self.request.GET['id']
        child_id = self.request.GET['child_id'] if 'child_id' in self.request.GET else None
        self.initial = {
            'id': application_id
        }

        api_response = NannyGatewayActions().list('your-children', params={
            'application_id': application_id})


        if 'child_id' in self.request.GET:
            self.initial['child_id'] = child_id

        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()

        kwargs['fields'] = [kwargs['form'].render_field(name, field) for name, field in kwargs['form'].fields.items()]
        kwargs['id'] = application_id
        kwargs['child_id'] = child_id

        return super(YourChildrenDetailsView, self).get_context_data(**kwargs)

    """
   Need functionality for the 'add' and 'remove' children features, also how the form will be rendered 
   within the page!
   """
