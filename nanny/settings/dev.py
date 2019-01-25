from .base import *

DEBUG = True

PAYMENT_URL = os.environ.get('APP_PAYMENT_URL', 'http://localhost:8001/payment-gateway')

ADDRESSING_URL = os.environ.get('APP_ADDRESSING_URL', 'http://localhost:8002/addressing-service')

NOTIFY_URL = os.environ.get('APP_NOTIFY_URL', 'http://localhost:8003/notify-gateway')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'nanny_db'),
        'USER': os.environ.get('POSTGRES_USER', 'ofs'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'ofs'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432')
    }
}

TEST_NOTIFY_CONNECTION = False

STATIC_URL = URL_PREFIX + '/static/'

PUBLIC_APPLICATION_URL = 'http://localhost:8000' + URL_PREFIX

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS +  PROJECT_APPS


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'ezn^k@w45@&zncvn)fzsrnke-e04s#+3$$ol$m=_nfwsfchlvp')

# Custom django debug toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'application.presentation.utilities.show_django_debug_toolbar',
}
