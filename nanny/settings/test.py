from .base import *

URL_PREFIX = '/nanny'

DEBUG = False

STATIC_URL = URL_PREFIX + '/static/'

ALLOWED_HOSTS = ['*']

# GTM Container ID
GOOGLE_TAG_MANAGER_ID = "GTM-MNCJ8QK"

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS

FEEDBACK_EMAIL = 'registrationpilot@ofsted.gov.uk'

SECRET_KEY = os.environ.get('SECRET_KEY', '!cpk9yyix!m9(jgc7ufreu-il0nj)p@w!l)g4cg@g8#-c9uq-p')