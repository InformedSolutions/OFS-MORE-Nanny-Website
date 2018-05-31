from .base import *


DEBUG = False

PROD_APPS = []

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', ')8a7c-wwy%xm=u2n#(whzdile^imbt)q89s+9!5d(ci=p=l+mm')
