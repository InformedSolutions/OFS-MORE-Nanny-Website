from .base import *


DEBUG = False

PROD_APPS = []

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS

FEEDBACK_EMAIL = 'registrationpilot@ofsted.gov.uk'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
