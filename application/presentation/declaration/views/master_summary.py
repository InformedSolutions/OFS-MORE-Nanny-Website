import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from application.presentation.base_views import NannyTemplateView
from application.presentation.utilities import build_url, NeverCacheMixin
from ....services.db_gateways import NannyGatewayActions


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

    @staticmethod
    def get_arc_flagged(application_id):
        """
        Get the related _arc_flagged database value for each task in the summary
        :param application_id: application_id for the user
        :return: Dictionary containing the section names along with their arc flagged status
        """
        application_response = NannyGatewayActions().read('application', {'application_id': application_id})
        db_arc_flagged = {}
        if application_response.status_code == 200 and application_response.record:
            application_record = application_response.record

            db_arc_flagged = {'user_details': application_record['login_details_arc_flagged'],
                            'applicant_personal_details_section': application_record['personal_details_arc_flagged'],
                            'applicant_home_address': application_record['personal_details_arc_flagged'],
                          'childcare_address_section': application_record['childcare_address_arc_flagged'],
                          'first_aid': application_record['first_aid_arc_flagged'],
                          'childcare_training': application_record['childcare_training_arc_flagged'],
                          'dbs_check': application_record['dbs_arc_flagged'],
                          'insurance_cover': application_record['insurance_cover_arc_flagged']}

        return db_arc_flagged, application_record


    def get_context_data(self):
        context = super().get_context_data()
        app_id = self.request.GET["id"]

        json = self.load_json(app_id, '', self.section_names, False)

        context['json'] = json
        context['application_id'] = app_id
        context['id'] = self.request.GET['id']
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
        arc_flagged = self.get_arc_flagged(app_id)
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
                            table_list = self.__parse_data(data_dict, app_id, section_key, section, recurse, table_list, arc_flagged)
                    else:
                        table_list = self.__parse_data(data, app_id, section_key, section, recurse, table_list, arc_flagged)

        if recurse:
            table_list = sorted(table_list, key=lambda k: k['index'])
        return table_list

    def __parse_data(self, data, app_id, section_key, section, recurse, table_list, arc_flagged):
        application_record = arc_flagged[1]
        arc_flagged_dict = arc_flagged[0]
        if application_record['application_status'] == "FURTHER_INFORMATION":
            if section in arc_flagged_dict and arc_flagged_dict[section]:
                data = self.generate_links(data, app_id)
            elif section_key in arc_flagged_dict and arc_flagged_dict[section_key]:
                data = self.generate_links(data, app_id)
        else:
            data = self.generate_links(data, app_id)
        new_data = [row for row in data if (not row.get('section') or row.get('section') == section_key)]

        if recurse:
            return table_list + new_data
        else:
            new_table_list = table_list
            new_table_list.append(new_data)
            return new_table_list
