from nanny.base_views import *
from nanny.utilities import *
from ..forms.public_liability import PublicLiabilityForm

from nanny_gateway import NannyGatewayActions


class PublicLiabilityView(NannyFormView):
    template_name = 'public-liability.html'
    success_url = ''
    form_class = PublicLiabilityForm

    def get_initial(self):
        initial = super().get_initial()
        app_id = app_id_finder(self.request)

        try:
            record = NannyGatewayActions().read('insurance-cover', params={'application_id': app_id})
            initial['public_liability'] = record['public_liability']
        except Exception as e:
            if e.error.title == '404 Not Found':
                pass
            else:
                raise e

        return initial

    def form_valid(self, form):
        app_id = app_id_finder(self.request)
        public_liability = form.cleaned_data['public_liability']

        try:
            NannyGatewayActions().patch('insurance-cover', params={'application_id': app_id,
                                                                 'public_liability': public_liability})
        except Exception as e:
            if e.error.title == '404 Not Found':
                NannyGatewayActions().create('insurance-cover', params={'application_id': app_id,
                                                                        'public_liability': public_liability})
            else:
                raise e

        if public_liability == 'True':
            self.success_url = 'insurance:Summary'
        elif public_liability == 'False':
            self.success_url = 'insurance:Insurance-Cover'

        # set status of insurance cover task to 'in progress'
        record = NannyGatewayActions().read('application', params={'application_id': app_id})
        record['insurance_cover_status'] = 'IN_PROGRESS'
        NannyGatewayActions().put('application', params=record)

        return super(PublicLiabilityView, self).form_valid(form)
