from coreapi.exceptions import ErrorMessage

from .base import BaseFormView
from ..forms.where_you_work import WhereYouWorkForm
from ..utils import *
from django.shortcuts import HttpResponseRedirect

from nanny_gateway import NannyGatewayActions


class WhereYouWorkView(BaseFormView):
    """
    Class containing the view(s) for handling the GET requests to the where you work page.
    """

    template_name = 'where-you-work.html'
    success_url = ''
    form_class = WhereYouWorkForm

    def form_valid(self, form):
        app_id = self.request.GET['id']

        record = NannyGatewayActions().read('application', params={'application_id': app_id})

        if form.cleaned_data['address_to_be_provided'] == 'True':
            record['address_to_be_provided'] = True
            self.success_url = 'Childcare-Address-Location'
        elif form.cleaned_data['address_to_be_provided'] == 'False':
            record['address_to_be_provided'] = False
            self.success_url = 'Childcare-Address-Details-Later'
        else:
            record['address_to_be_provided'] = None

        record['childcare_address_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=record)

        try:
            NannyGatewayActions().list('childcare-address', params={'application_id': app_id})
            return HttpResponseRedirect(build_url('Childcare-Address-Details', get={'id': app_id}))
        except ErrorMessage as e:
            if e.error.title == '404 Not Found':
                pass
            else:
                raise e

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