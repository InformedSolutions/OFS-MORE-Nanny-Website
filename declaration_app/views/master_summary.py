import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from nanny import NannyGatewayActions
from nanny.base_views import NannyTemplateView
from nanny.utilities import build_url, NeverCacheMixin


class MasterSummary(NeverCacheMixin, NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    template_name = "master-summary.html"
    success_url_name = 'declaration:Declaration-Guidance'
    model_names = {"applicant_personal_details_section": ["applicant_personal_details", "applicant_home_address"],
                   "childcare_address_section": ["application", "applicant_home_address", "childcare_address"]
                   }
    # Note that section_names is updated at get_context_data.
    section_names = ["user_details", "applicant_personal_details_section", "childcare_address_section",
                     "first_aid", "childcare_training", "dbs_check", "insurance_cover"]

    def get_context_data(self):
        context = super().get_context_data()
        app_id = self.request.GET["id"]

        self.section_names = self.__update_section_names(self.section_names, app_id)
        json = self.load_json(app_id, '', self.section_names, False)

        context['json'] = json
        context['application_id'] = app_id
        context['id'] = self.request.GET['id']
        return context

    @staticmethod
    def __update_section_names(section_names, app_id):
        """
        Updates section_names to include childcare address if the your_children task is present.
        :return: New section_names list
        """
        applicant_person_details_record = NannyGatewayActions().read('applicant-personal-details',
                                                                     params={'application_id': app_id}).record
        if applicant_person_details_record.get('your_children') and 'your_children' not in section_names:
            section_names.insert(2, 'your_children')

        return section_names

    def post(self, request):
        return HttpResponseRedirect(build_url(self.success_url_name, get={'id': request.GET['id']}))

    def generate_links(self, json, app_id):
        for table in json:
            if isinstance(table, list):
                self.generate_links(table, app_id)
            else:
                if 'reverse' in table.keys():
                    table['link'] = reverse(table['reverse']) + '?id=' + app_id
                    if 'extra_reverse_params' in table.keys():
                        for extra_param in table['extra_reverse_params']:
                            param_name, param_val = extra_param
                            table['link'] += "&{0}={1}".format(param_name, param_val)
        return json

    def load_json(self, app_id, section_key, section_names, recurse):
        """
        Dynamically builds a JSON to be consumed by the HTML summary page
        :param app_id: the id of the application being handled
        :param section_key: only set if recurse is true, the section name where the current task is being rendered
        :param section_names: the models to be built for the summary page
        :param recurse: flag to indicate whether the method is currently recursing
        :return:
        """
        nanny_url = settings.APP_NANNY_GATEWAY_URL
        identity_url = settings.APP_IDENTITY_URL
        table_list = []
        for section in section_names:
            if self.model_names.get(section):
                table_list.append(self.load_json(app_id, section, self.model_names.get(section), True))
            else:
                if section == "user_details":
                    response = requests.get(identity_url + "api/v1/summary/" + str(section) + "/" + str(app_id))
                else:
                    response = requests.get(nanny_url + "/api/v1/summary/" + str(section) + "/" + str(app_id))
                if response.status_code == 200:
                    data = response.json()
                    # Support for multiple tables being returned for one section
                    if type(data[0]) == list and len(data) > 1:
                        for data_dict in data:
                            table_list = self.__parse_data(data_dict, app_id, section_key, recurse, table_list)
                    else:
                        table_list = self.__parse_data(data, app_id, section_key, recurse, table_list)

        if recurse:
            table_list = sorted(table_list, key=lambda k: k['index'])
        return table_list

    def __parse_data(self, data, app_id, section_key, recurse, table_list):
        data = self.generate_links(data, app_id)
        new_data = [row for row in data if (not row.get('section') or row.get('section') == section_key)]

        if recurse:
            return table_list + new_data
        else:
            new_table_list = table_list
            new_table_list.append(new_data)
            return new_table_list
