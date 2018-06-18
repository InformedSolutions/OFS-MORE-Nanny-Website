from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse

from nanny_models.application import Application


def redirect_by_status(application_id):
    """
    Helper method to calculate a redirect that a user should be issued after logging in
    based on an application's current status
    :param application_id:
    :return: an HttpResponseRedirect to a landing page based on an application's current status
    """

    api_response = Application.api.get_record(application_id=application_id)

    if api_response.status_code != 200:
        response = HttpResponseRedirect(
            reverse('Contact-Details-Summary') + '?id=' + str(application_id))
        return response

    application = api_response.record

    if application['application_status'] == 'DRAFTING':
        if application['login_details_status'] == 'COMPLETED':
            response = HttpResponseRedirect(
                reverse('Task-List') + '?id=' + str(application_id)
            )
        else:
            response = HttpResponseRedirect(
                reverse('Contact-Details-Summary') + '?id=' + str(application_id)
            )

    return response
