from .base import *


DEBUG = False

PROD_APPS = []

ALLOWED_HOSTS = ['*']

STATIC_URL = URL_PREFIX + '/static/'

# GTM Container ID
GOOGLE_TAG_MANAGER_ID = ""

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS

FEEDBACK_EMAIL = 'Registrationfeedback@ofsted.gov.uk'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
