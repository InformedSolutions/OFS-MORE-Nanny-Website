from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = "127.0.0.1"

DEV_APPS = [
    'debug_toolbar'
]

MIDDLEWARE_DEV = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

URL_PREFIX = '/nanny'

STATIC_URL = URL_PREFIX + '/static/'

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + DEV_APPS + PROJECT_APPS
MIDDLEWARE = MIDDLEWARE + MIDDLEWARE_DEV

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ezn^k@w45@&zncvn)fzsrnke-e04s#+3$$ol$m=_nfwsfchlvp')