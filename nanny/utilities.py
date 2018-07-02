"""
Generic helper functions
"""
from django.conf import settings
from django.urls import reverse
from urllib.parse import urlencode


def show_django_debug_toolbar(request):
    """
    Custom callback function to determine whether the django debug toolbar should be shown
    :param request: inbound HTTP request
    :return: boolean indicator used to trigger visibility of debug toolbar
    """
    return settings.DEBUG


def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urlencode(get)
    return url


def app_id_finder(request):
    app_id = None
    if request.GET.get('id'):
        app_id = request.GET.get('id')
    if request.POST.get('id'):
        app_id = request.POST.get('id')

    return(app_id)

# TEST UTILTIIES #


class CustomResponse:
    record = None

    def __init__(self, record):
        self.record = record


def authenticate(application_id):
    record = {
            'application_id': application_id,
            'email': 'test@informed.com'
        }
    return CustomResponse(record)