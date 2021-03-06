import socket

from .base import *

DEBUG = True

SESSION_COOKIE_SECURE = False

TEST_NOTIFY_CONNECTION = False

STATIC_URL = URL_PREFIX + '/static/'

PUBLIC_APPLICATION_URL = 'http://localhost:8000' + URL_PREFIX

ALLOWED_HOSTS = ['*']

# GTM Container ID
GOOGLE_TAG_MANAGER_ID = "GTM-545782K"

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS

FEEDBACK_EMAIL = 'tester@informed.com'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ezn^k@w45@&zncvn)fzsrnke-e04s#+3$$ol$m=_nfwsfchlvp')

# Custom django debug toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'application.presentation.utilities.show_django_debug_toolbar',
}
