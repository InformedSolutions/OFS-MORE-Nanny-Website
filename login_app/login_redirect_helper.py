from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse

from tasks_app.models import NannyApplication


def redirect_by_status(application_id):
    """
    Helper method to calculate a redirect that a user should be issued after logging in
    based on an application's current status
    :param application_id:
    :return: an HttpResponseRedirect to a landing page based on an application's current status
    """
    try:
        application = NannyApplication.objects.get(pk=application_id)
    except ObjectDoesNotExist:
        response = HttpResponseRedirect(
            reverse('Contact-Details-Summary') + '?id=' + str(application_id))
        return response

    if application.application_status == 'DRAFTING':
        if application.login_details_status == 'COMPLETED':
            response = HttpResponseRedirect(
                reverse('Task-List') + '?id=' + str(application_id)
            )
        else:
            response = HttpResponseRedirect(
                reverse('Contact-Details-Summary') + '?id=' + str(application_id))

    return response
