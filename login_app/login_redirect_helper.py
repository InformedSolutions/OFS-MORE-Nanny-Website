from django.http import HttpResponseRedirect
from django.urls import reverse

from nanny.db_gateways import NannyGatewayActions


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

    if app_record['application_status'] == 'DRAFTING':
        if app_record['login_details_status'] == 'COMPLETED':
            response = HttpResponseRedirect(
                reverse('Task-List') + '?id=' + str(application_id)
            )
        else:
            response = HttpResponseRedirect(
                reverse('Contact-Details-Summary') + '?id=' + str(application_id))

    elif app_record['application_status'] == 'SUBMITTED':
        response = HttpResponseRedirect(
            reverse('declaration:confirmation') + '?id=' + str(application_id))

    return response
