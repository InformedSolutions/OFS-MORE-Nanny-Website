from django.http import HttpResponseRedirect
from django.urls import reverse

from application.services.db_gateways import NannyGatewayActions


def redirect_by_status(application_id):
    """
    Helper method to calculate a redirect that a user should be issued after logging in
    based on an application's current status
    :param application_id:
    :return: an HttpResponseRedirect to a landing page based on an application's current status
    """
    try:
        app_record = NannyGatewayActions().read('application', params={'application_id': application_id}).record
    except AttributeError:
        return HttpResponseRedirect(reverse('Contact-Details-Summary') + '?id=' + str(application_id))
    status = app_record['application_status']
    if status == 'DRAFTING':
        if app_record['personal_details_status'] == 'COMPLETED':
            response = HttpResponseRedirect(
                reverse('Task-List') + '?id=' + str(application_id)
            )
        else:
            response = HttpResponseRedirect(
                reverse('Contact-Details-Summary') + '?id=' + str(application_id))

    elif status == 'SUBMITTED' or status == 'ARC_REVIEW':
        response = HttpResponseRedirect(
            reverse('declaration:confirmation') + '?id=' + str(application_id))

    elif status == 'FURTHER_INFORMATION':
            response = HttpResponseRedirect(
                reverse('Task-List') + '?id=' + str(application_id)
            )

    # default to task list
    else:
        response = HttpResponseRedirect(
            reverse('Task-List') + '?id=' + str(application_id)
        )

    return response
