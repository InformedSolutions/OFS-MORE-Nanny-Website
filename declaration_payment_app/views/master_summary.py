from first_aid_app.views.base import BaseTemplateView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import reverse
from nanny.utilities import build_url
import requests
import simplejson


class MasterSummary(BaseTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "master-summary.html"
    success_url_name = 'declaration-payment:Declaration-Guidance'
    model_names = ["user_details", ["applicant_personal_details", "applicant_home_address"], ["application","childcare_address"],
                   "first_aid", "childcare_training", "dbs_check", "insurance_cover"]

    def get_context_data(self):
        context = super().get_context_data()
        app_id = self.request.GET["id"]
        json = self.load_json(app_id, self.model_names, False)
        context['json'] = json
        context['application_id'] = app_id
        return context

    def post(self, request):
        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': request.GET['id']}))

    def generate_links(self, json, app_id):
        for table in json:
            if isinstance(table, list):
                self.generate_links(table, app_id)
            else:
                if 'reverse' in table.keys():
                    table['link'] = reverse(table['reverse']) + '?id=' + app_id
        return json

    def load_json(self, app_id, ordered_models, recurse):
        """
        Dynamically builds a JSON to be consumed by the HTML summary page
        :param app_id: the id of the application being handled
        :param ordered_models: the models to be built for the summary page
        :param recurse: flag to indicate whether the method is currently recursing
        :return:
        """
        nanny_url = settings.APP_NANNY_GATEWAY_URL
        identity_url = settings.APP_IDENTITY_URL
        table_list = []
        for model in ordered_models:
            if isinstance(model, list):
                table_list.append(self.load_json(app_id, model, True))
            else:
                if model == "user_details":
                    response = requests.get(identity_url + "api/v1/summary/" + str(model) + "/" + str(app_id))
                else:
                    response = requests.get(nanny_url + "/api/v1/summary/" + str(model) + "/" + str(app_id))
                if response.status_code == 200:
                    data = simplejson.loads(response.content)
                    data = self.generate_links(data, app_id)
                    if recurse:
                        table_list = table_list + data
                    else:
                        table_list.append(data)

        if recurse:
            table_list = sorted(table_list, key=lambda k: k['index'])
        return table_list
