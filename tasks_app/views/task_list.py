from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from django.views.decorators.cache import never_cache

from nanny.db_gateways import NannyGatewayActions


def show_hide_tasks(context, application, application_id):
    """
    Method hiding or showing the your children tasks based on whether the applicant has children
    :param context: a dictionary containing all tasks for the task list
    :param context: Application object
    :return: dictionary object
    """

    for task in context['tasks']:
        if task['name'] == 'your_children':

            nanny_api_response = NannyGatewayActions().read('applicant-personal-details',
                                                            params={'application_id': application_id})
            if nanny_api_response.status_code == 200:
                application = nanny_api_response.record
            else:
                if settings.DEBUG:
                    raise RuntimeError('The nanny-gateway API did not respond as expected.')
                else:
                    HttpResponseRedirect(reverse('Service-Unavailable'))

            # If the applicant has children under 16, reveal the 'your children' task
            if application['your_children'] is True:
                task['hidden'] = False
            else:
                task['hidden'] = True

        # If the task is not conditionally revealed, set the 'hidden' flag to false
        # This allows the declaration task to be unlocked correctly
        else:
            task['hidden'] = False

    return context


class TaskListView(View):
    @never_cache
    def get(self, request):
        application_id = request.GET["id"]
        nanny_api_response = NannyGatewayActions().read('application', params={'application_id': application_id})
        if nanny_api_response.status_code == 200:
            application = nanny_api_response.record
        else:
            if settings.DEBUG:
                raise RuntimeError('The nanny-gateway API did not respond as expected.')
            else:
                HttpResponseRedirect(reverse('Service-Unavailable'))

        status = application.get('application_status')
        # Add handlers to prevent a user re-accessing their application details and modifying post-submission
        if status == 'ARC_REVIEW' or status == 'SUBMITTED':
            return HttpResponseRedirect(
                reverse('declaration:confirmation') + '?id=' + str(application['application_id'])
            )

        if status == 'ACCEPTED':
            return HttpResponseRedirect(
                reverse('declaration:accepted-confirmation') + '?id=' + str(application['application_id'])
            )

        context = {
            'id': application_id,
            'all_complete': False,
            'application_status': application['application_status'],
            'tasks': [
                {
                    'name': 'account_details',  # This is CSS class (Not recommended to store it here)
                    'status': application['login_details_status'],
                    'arc_flagged': application['login_details_arc_flagged'],
                    'description': "Your sign in details",
                    'status_url': 'Contact-Details-Summary',
                },
                {
                    'name': 'personal_details',
                    'status': application['personal_details_status'],
                    'arc_flagged': application['personal_details_arc_flagged'],
                    'description': 'Your personal details',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'personal-details:Personal-Details-Summary',
                        'NOT_COMPLETED': 'personal-details:Personal-Details-Name'
                    }

                },
                {  # This is using placeholder details to populate fields as the task is not yet created
                    # and this currently mirrors the links and status of the 'childcare address' task
                    'name': 'your_children',
                    'status': application['your_children_status'],
                    'arc_flagged': application['your_children_arc_flagged'],
                    'description': 'Your children',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'Your-Children-Guidance',
                        'NOT_COMPLETED': 'Your-Children-Guidance',
                    }

                },
                {
                    'name': 'childcare_address',
                    'status': application['childcare_address_status'],
                    'arc_flagged': application['childcare_address_arc_flagged'],
                    'description': 'Childcare address',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'Childcare-Address-Summary',
                        'NOT_COMPLETED': 'Childcare-Address-Guidance'
                    }

                },
                {
                    'name': 'first_aid_training',
                    'status': application['first_aid_status'],
                    'arc_flagged': application['first_aid_arc_flagged'],
                    'description': 'First aid training',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'first-aid:First-Aid-Summary',
                        'NOT_COMPLETED': 'first-aid:First-Aid-Guidance'
                    }
                },
                {
                    'name': 'childcare_training',
                    'status': application['childcare_training_status'],
                    'arc_flagged': application['childcare_training_arc_flagged'],
                    'description': 'Childcare training',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'Childcare-Training-Summary',
                        'NOT_COMPLETED': 'Childcare-Training-Guidance'
                    }
                },
                {
                    'name': 'criminal_record',
                    'status': application['dbs_status'],
                    'arc_flagged': application['dbs_arc_flagged'],
                    'description': 'Criminal record checks',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'dbs:Summary',
                        'NOT_COMPLETED': 'dbs:Criminal-Record-Checks-Guidance-View'
                    }
                },
                {
                    'name': 'insurance_cover',
                    'status': application['insurance_cover_status'],
                    'arc_flagged': application['insurance_cover_arc_flagged'],
                    'description': 'Insurance cover',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'insurance:Summary',
                        'NOT_COMPLETED': 'insurance:Guidance'
                    }
                },
                {
                    'name': 'review',
                    'status': 'DO_LAST',
                    'arc_flagged': application['application_status'],
                    # If application is being resubmitted (i.e. is not drafting,
                    # set declaration task name to read "Declaration" only)
                    'description':
                        "Declaration and payment" if application['application_status'] == 'DRAFTING' else "Declaration",
                    'status_url': '',
                },
            ]
        }

        context = show_hide_tasks(context, application, application_id)

        context['all_complete'] = all(
            task['status'] == 'COMPLETED' for task in context['tasks'][:-1] if not task['hidden'])

        if context['all_complete']:
            context['tasks'][-1]['status'] = 'NOT_STARTED'
            context['tasks'][-1]['status_url'] = 'declaration:Master-Summary'

        for task in context['tasks'][1:-1]:
            task['status_url'] = task['status_urls']['COMPLETED/FLAGGED'] if task['status'] in (
            'COMPLETED', 'FLAGGED') else task['status_urls']['NOT_COMPLETED']

        return render(request, 'task-list.html', context)
