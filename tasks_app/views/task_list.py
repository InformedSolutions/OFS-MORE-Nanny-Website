from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from django.views.decorators.cache import never_cache
import uuid

from nanny_models.nanny_application import NannyApplication

from identity_models.user_details import UserDetails


class TaskListView(View):
    @never_cache
    def get(self, request):
        application_id = request.GET["id"]
        identity_api_response = UserDetails.api.get_record(application_id=application_id)
        record = identity_api_response.record
        email_address = record['email']
        nanny_api_response = NannyApplication.api.get_record(application_id=application_id)
        if nanny_api_response.status_code == 200:
            application = NannyApplication(**nanny_api_response.record)
        elif nanny_api_response.status_code == 404:
            application = create_new_app(application_id=application_id)
        else:
            if settings.DEBUG:
                raise RuntimeError('The nanny-gateway API did not respond as expected.')
            else:
                HttpResponseRedirect(reverse('Service-Down'))

        context = {
            'id': application_id,
            'email_address': email_address,
            'all_complete': False,
            'application_status': application.application_status,
            'tasks': [
                {
                    'name': 'account_details',  # This is CSS class (Not recommended to store it here)
                    'status': application.login_details_status,
                    'arc_flagged': application.login_details_arc_flagged,
                    'description': "Your sign in details",
                    'status_url': None,  # Will be filled later
                    'status_urls': [  # Available urls for each status
                        {'status': 'COMPLETED', 'url': 'Contact-Details-Summary'},
                        {'status': 'FLAGGED', 'url': 'Contact-Details-Summary'},
                        {'status': 'OTHER', 'url': 'Contact-Details-Summary'},  # For all other statuses
                    ],
                },
                {
                    'name': 'personal_details',
                    'status': application.personal_details_status,
                    'arc_flagged': application.personal_details_arc_flagged,
                    'description': 'Your personal details',
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Personal-Details-Summary'},
                        {'status': 'FLAGGED', 'url': 'Personal-Details-Summary'},
                        {'status': 'OTHER', 'url': 'Personal-Details-Guidance'},  # For all other statuses
                    ]
                },
                {
                    'name': 'childcare_address',
                    'status': application.childcare_address_status,
                    'arc_flagged': application.childcare_address_arc_flagged,
                    'description': 'Childcare address',
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Childcare-Address-Summary'},
                        {'status': 'FLAGGED', 'url': 'Childcare-Address-Summary'},
                        {'status': 'OTHER', 'url': 'Childcare-Address-Guidance'},  # For all other statuses
                    ]
                },
                {
                    'name': 'first_aid_training',
                    'status': application.first_aid_training_status,
                    'arc_flagged': application.first_aid_training_arc_flagged,
                    'description': 'First aid training',
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'first-aid:First-Aid-Summary'},
                        {'status': 'FLAGGED', 'url': 'first-aid:First-Aid-Summary'},
                        {'status': 'OTHER', 'url': 'first-aid:First-Aid-Guidance'},  # For all other statuses
                    ]
                },
                {
                    'name': 'childcare_training',
                    'status': application.childcare_training_status,
                    'arc_flagged': application.childcare_training_arc_flagged,
                    'description': 'Childcare training',
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Childcare-Training-Summary'},
                        {'status': 'FLAGGED', 'url': 'Childcare-Training-Summary'},
                        {'status': 'OTHER', 'url': 'Childcare-Training-Guidance'},  # For all other statuses
                    ]
                },
                {
                    'name': 'criminal_record',
                    'status': application.criminal_record_check_status,
                    'arc_flagged': application.criminal_record_check_arc_flagged,
                    'description': 'Criminal record (DBS) check',
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Criminal-Record-Summary'},
                        {'status': 'FLAGGED', 'url': 'Criminal-Record-Summary'},
                        {'status': 'OTHER', 'url': 'Criminal-Record-Guidance'},  # For all other statuses
                    ]
                },
                {
                    'name': 'insurance_cover',
                    'status': application.insurance_cover_status,
                    'arc_flagged': application.insurance_cover_arc_flagged,
                    'description': 'Insurance cover',
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Insurance-Cover-Summary'},
                        {'status': 'FLAGGED', 'url': 'Insurance-Cover-Summary'},
                        {'status': 'OTHER', 'url': 'Insurance-Cover-Guidance'},  # For all other statuses
                    ]
                },
                {
                    'name': 'review',
                    'status': None,
                    'arc_flagged': application.application_status,
                    # If application is being resubmitted (i.e. is not drafting,
                    # set declaration task name to read "Declaration" only)
                    'description':
                        "Declaration and payment" if application.application_status == 'DRAFTING' else "Declaration",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Declaration-Declaration-View'},
                        {'status': 'OTHER', 'url': 'Declaration-Summary'}
                    ],
                },
            ]
        }

        if len([task for task in context['tasks'] if task['status'] in ['IN_PROGRESS', 'NOT_STARTED', 'FLAGGED', 'WAITING']]) < 1:
            context['all_complete'] = True
        else:
            context['all_complete'] = False

        if context['all_complete']:
            # Set declaration status to NOT_STARTED
            for task in context['tasks']:
                if task['name'] == 'review':
                    if task['status'] is None:
                        task['status'] = application.declarations_status

        # Prepare task links

        for task in context['tasks']:

            # Iterating through tasks

            for url in task.get('status_urls'):  # Iterating through task available urls
                if url['status'] == task['status']:  # Match current task status with url which is in status_urls
                    task['status_url'] = url['url']  # Set main task primary url to the one which matched

            if not task['status_url']:  # In case no matches were found by task status
                for url in task.get('status_urls'):  # Search for link with has status "OTHER"
                    if url['status'] == "OTHER":
                        task['status_url'] = url['url']

        return render(request, 'task-list.html', context)


def create_new_app(application_id):
    """
    Create a new NannyApplication model in the db with the application_id argument as specified.
    :return; NannyApplication model if nanny-gateway created record successfully, else redirect to 'Service-Down' page.
    """
    application_id = uuid.UUID(application_id)
    api_response_create = NannyApplication.api.create(
        application_id=application_id,
        application_status='DRAFTING',
        login_details_status='COMPLETED',
        model_type=NannyApplication
    )
    if api_response_create.status_code == 201:
        response = NannyApplication.api.get_record(
            application_id=application_id
        )
        return NannyApplication(**response.record)
    else:
        if settings.DEBUG:
            raise RuntimeError('The nanny-gateway API did not respond as expected.')
        else:
            HttpResponseRedirect(reverse('Service-Down'))
