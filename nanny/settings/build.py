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

# Automatic Django logging at the INFO level (i.e everything the comes to the console when ran locally)
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        },
  'handlers': {
    'file': {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'maxBytes': 1 * 1024 * 1024,
        'filename': 'logs/output.log',
        'formatter': 'console',
        'maxBytes': 1 * 1024 * 1024,
        'backupCount': '30'
    },
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler'
    },
   },
   'loggers': {
     'django': {
       'handlers': ['file', 'console'],
         'level': 'INFO',
           'propagate': True,
      },
      'django.server': {
       'handlers': ['file', 'console'],
         'level': 'INFO',
           'propagate': True,
      },
      'payment_app.views.payment': {
       'handlers': ['file', 'console'],
         'level': 'DEBUG',
           'propagate': True,
      },
    },

}
