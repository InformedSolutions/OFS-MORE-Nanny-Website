from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from django.views.decorators.cache import never_cache

from nanny.db_gateways import NannyGatewayActions


class TaskListView(View):
    @never_cache
    def get(self, request):
        application_id = request.GET["id"]
        application = None
        nanny_api_response = NannyGatewayActions().read('application', params={'application_id': application_id})

        if nanny_api_response.status_code == 200:
            application = nanny_api_response.record

        elif nanny_api_response.status_code == 404:
            create_response = NannyGatewayActions().create(
                'application',
                params={
                    'application_id': application_id,
                    'application_status': 'DRAFTING',
                    'login_details_status': 'COMPLETED',
                }
            )
            application = create_response.record

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
                        'NOT_COMPLETED': 'First-Aid-Guidance'
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
                    'description': 'Criminal record (DBS) check',
                    'status_url': None,
                    'status_urls': {
                        'COMPLETED/FLAGGED': 'dbs:Summary',
                        'NOT_COMPLETED': 'dbs:Guidance'
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

        context['all_complete'] = all(task['status'] == 'COMPLETED' for task in context['tasks'][:-1])

        if context['all_complete']:
            context['tasks'][-1]['status'] = 'NOT_STARTED'
            context['tasks'][-1]['status_url'] = 'declaration:Master-Summary'

        for task in context['tasks'][1:-1]:
            task['status_url'] = task['status_urls']['COMPLETED/FLAGGED'] if task['status'] in ('COMPLETED', 'FLAGGED') else task['status_urls']['NOT_COMPLETED']

        return render(request, 'task-list.html', context)
