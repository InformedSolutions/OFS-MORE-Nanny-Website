import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render

from ...base_views import NannyTemplateView
from application.presentation.utilities import *
from ....services.db_gateways import NannyGatewayActions, IdentityGatewayActions
from application.services.notify import send_email
from ...utilities import app_id_finder, get_confirmation_page_template, get_confirmation_status
from ... payment.views.payment import check_tasks_completed

logger = logging.getLogger()


class Confirmation(NannyTemplateView):
    """
    Template view to  render the guidance page from first access of task from task list
    """
    def get(self, request, *args, **kwargs):
        """
        On a post request, set the task status to completed and redirect the user to the task list
        :return:
        """
        application_id = app_id_finder(request)
        application_response = NannyGatewayActions().read('application', params={'application_id': application_id})
        if application_response.status_code == 200:
            application_record = application_response.record
            app_status = application_record['application_status']
            if (app_status in ['DRAFTING', 'FURTHER_INFORMATION'])  and not check_tasks_completed(application_record, include_payment=True):
                return HttpResponseRedirect(reverse('Task-List') + '?id=' + application_id)
            else:
                context = self.get_context_data(**kwargs)
                template_name = self.get_template_names()
                return render(request, template_name, context)

    def get_context_data(self, **kwargs):
        app_id = app_id_finder(self.request)
        cost = '103.00'
        api_app_response = NannyGatewayActions().read('application', params={'application_id': app_id})

        context = {
            'id': app_id,
            'cost': cost
        }

        if api_app_response.status_code == 200:
            application_record = api_app_response.record

            context['application_reference'] = application_record['application_reference']

            # Check for ARC_REVIEW to prevent resetting the status of apps assigned to a reviewer.
            if application_record['application_status'] != 'ARC_REVIEW':
                api_pd_response = NannyGatewayActions().read('applicant-personal-details',
                                                             params={'application_id': app_id})

                if api_pd_response.status_code == 200:
                    personal_details_record = api_pd_response.record

                    if application_record['application_status'] == 'DRAFTING':
                        self.send_survey_email(app_id, personal_details_record, application_record)

                application_record['application_status'] = 'SUBMITTED'
                NannyGatewayActions().put('application', params=application_record)

        else:
            raise ValueError('Nanny-Gateway returned {0} response for "application" endpoint, not 200'.format(
                api_app_response.status_code))

        context['id'] = app_id
        return context

    def get_template_names(self):
        app_id = app_id_finder(self.request)
        dbs_record = NannyGatewayActions().read('dbs-check', params={'application_id': app_id}).record

        capita = dbs_record['is_ofsted_dbs']
        certificate_information = dbs_record['certificate_information']
        lived_abroad = dbs_record['lived_abroad']

        confirmation_status = get_confirmation_status(capita, certificate_information, lived_abroad)
        template_name = get_confirmation_page_template(confirmation_status)

        return template_name

    @staticmethod
    def send_survey_email(application_id, personal_details_record, application_record):
        """
        function to get user's details and send them the survey email on confirmation of their payment
        :param application_id:
        :param personal_details_record:
        :param application_record:
        """
        survey_template_id = 'ca1acc2f-cfc7-4d20-b5d6-5bb17fce1d0a'
        user_details_response = IdentityGatewayActions().read('user', params={'application_id': application_id})

        if user_details_response.status_code == 200:
            email = user_details_response.record['email']

            survey_personalisation = {
                'first_name': personal_details_record['first_name'], 'ref': application_record['application_reference']
            }

            logger.debug("Attempting to send survey email: What do you think of our service? - Applicant")
            send_email(email, survey_personalisation, survey_template_id)
