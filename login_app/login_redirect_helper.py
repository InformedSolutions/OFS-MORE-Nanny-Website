from django.http import HttpResponseRedirect
from django.urls import reverse

from nanny_models.nanny_application import NannyApplication


def redirect_by_status(application_id):
    """
    Helper method to calculate a redirect that a user should be issued after logging in
    based on an application's current status
    :param application_id:
    :return: an HttpResponseRedirect to a landing page based on an application's current status
    """
    app_record = NannyApplication.api.get_record(application_id=application_id).record

    if app_record is None:
        response = HttpResponseRedirect(
            reverse('Contact-Details-Summary') + '?id=' + str(application_id)
        )
    else:
        if app_record['application_status'] == 'DRAFTING':
            if app_record['login_details_status'] == 'COMPLETED':
                response = HttpResponseRedirect(
                    reverse('Task-List') + '?id=' + str(application_id)
                )
            else:
                response = HttpResponseRedirect(
                    reverse('Contact-Details-Summary') + '?id=' + str(application_id))

    return response
