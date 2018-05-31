"""
Generic helper functions
"""
from django.conf import settings


def show_django_debug_toolbar(request):
    """
    Custom callback function to determine whether the django debug toolbar should be shown
    :param request: inbound HTTP request
    :return: boolean indicator used to trigger visibility of debug toolbar
    """
    return settings.DEBUG
