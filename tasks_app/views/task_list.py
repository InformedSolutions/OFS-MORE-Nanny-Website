from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.decorators.cache import never_cache

from tasks_app.models import Application

from identity_models.user_details import UserDetails


# @never_cache
class TaskListView(View):
    def get(self, request):
        application_id = request.GET["id"]
        api_response = UserDetails.api.get_record(application_id=application_id)
        record = api_response.record
        email_address = record['email']

        try:
            application = Application.objects.get(pk=application_id)
        except ObjectDoesNotExist:
            application = create_new_app(app_id=application_id)

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
                        {'status': 'COMPLETED', 'url': 'First-Aid-Summary'},
                        {'status': 'FLAGGED', 'url': 'First-Aid-Summary'},
                        {'status': 'OTHER', 'url': 'First-Aid-Guidance'},  # For all other statuses
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


def create_new_app(app_id):
    application = Application.objects.create(
        application_id=app_id,
        application_type='NANNY',
        application_status='DRAFTING',
        cygnum_urn='',
        login_details_status='NOT_STARTED',
        personal_details_status='NOT_STARTED',
        childcare_type_status='NOT_STARTED',
        first_aid_training_status='NOT_STARTED',
        eyfs_training_status='NOT_STARTED',
        criminal_record_check_status='NOT_STARTED',
        health_status='NOT_STARTED',
        references_status='NOT_STARTED',
        people_in_home_status='NOT_STARTED',
        declarations_status='NOT_STARTED',
        date_created=timezone.now(),
        date_updated=timezone.now(),
        date_accepted=None,
        application_reference=None
    )
    # user = UserDetails.objects.create(application_id=application)

    # TimelineLog.objects.create(
    #     content_object=application,
    #     user=None,
    #     template='timeline_logger/application_action.txt',
    #     extra_data={'user_type': 'applicant', 'action': 'created', 'entity': 'application'}
    # )

    return application
