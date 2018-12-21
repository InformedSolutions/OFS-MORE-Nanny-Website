"""
Django settings for app-nanny  project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from nanny.logging import skip_starting_http_connection_logs

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

URL_PREFIX = '/nanny'

# Server name for showing server that responded to request under load balancing conditions
SERVER_LABEL = os.environ.get('SERVER_LABEL')

# Visa Validation
VISA_VALIDATION = os.environ.get('VISA_VALIDATION') == 'True'

# Base URL of notify gateway
NOTIFY_URL = os.environ.get('APP_NOTIFY_URL')

# Base URL of payment gateway
PAYMENT_URL = os.environ.get('APP_PAYMENT_URL')

# Payment specific settings
PAYMENT_PROCESSING_ATTEMPTS = os.environ.get('PAYMENT_PROCESSING_ATTEMPTS', 10)
PAYMENT_STATUS_QUERY_INTERVAL_IN_SECONDS = os.environ.get('PAYMENT_STATUS_QUERY_INTERVAL_IN_SECONDS', 10)

PAYMENT_HTTP_REQUEST_TIMEOUT = 60

# Base URL of addressing-service gateway
ADDRESSING_URL = os.environ.get('APP_ADDRESSING_URL')

# Base URL of nanny gateway
APP_NANNY_GATEWAY_URL = os.environ.get('APP_NANNY_GATEWAY_URL')

# Base URL of nanny gateway
APP_IDENTITY_URL = os.environ.get('APP_IDENTITY_URL')

PUBLIC_APPLICATION_URL = os.environ.get('PUBLIC_APPLICATION_URL')

EXECUTING_AS_TEST = os.environ.get('EXECUTING_AS_TEST', False)

TEST_NOTIFY_CONNECTION = True

# URL prefix for the identity-gateway API.
IDENTITY_URL_PREFIX = ""

# Expiry period of Magic Link Emails and Texts in hours
SMS_EXPIRY = 1
EMAIL_EXPIRY = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'database.sqlite'),
    }
}

# Application definition

BUILTIN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'govuk_template_base',
    'govuk_template',
    'govuk_forms',
    'google_analytics',
]

PROJECT_APPS = [
    'application.apps.ApplicationConfig',
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'nanny.middleware.CustomAuthenticationHandler',
]

ROOT_URLCONF = 'nanny.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR,
            os.path.join(BASE_DIR, 'nanny/generic_templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "nanny.middleware.globalise_url_prefix",
                "nanny.middleware.globalise_authentication_flag",
                'govuk_template_base.context_processors.govuk_template_base'
            ],
        },
    },
]

WSGI_APPLICATION = 'nanny.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'nanny', 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'nanny', 'staticfiles')

# Test outputs
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_VERBOSE = True
TEST_OUTPUT_DESCRIPTIONS = True
TEST_OUTPUT_DIR = 'xmlrunner'

# Output all logs to /logs directory
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
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/output.log'),
            'formatter': 'console',
            'when': 'midnight',
            'backupCount': 10
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'filters': {
        'urllib3_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_starting_http_connection_logs,
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'urllib3.connectionpool': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['urllib3_filter'],
        },
    },
}

# Export Settings variables DEBUG to templates context
SETTINGS_EXPORT = [
    'DEBUG'
]

AUTHENTICATION_URL = URL_PREFIX + '/sign-in/'

AUTHENTICATION_EXEMPT_URLS = (
    r'^' + URL_PREFIX + '$',
    r'^' + URL_PREFIX + '/$',
    r'^' + URL_PREFIX + '/register-as-nanny/$',
    r'^' + URL_PREFIX + '/account/account/$',
    r'^' + URL_PREFIX + '/account/email/$',
    r'^' + URL_PREFIX + '/security-question/$',
    r'^' + URL_PREFIX + '/email-sent/$',
    r'^' + URL_PREFIX + '/validate/.*$',
    r'^' + URL_PREFIX + '/code-resent/.*$',
    r'^' + URL_PREFIX + '/security-code/.*$',
    r'^' + URL_PREFIX + '/link-used/$',
    r'^' + URL_PREFIX + '/new-code/.*$',
    r'^' + URL_PREFIX + '/djga/+',
    r'^' + URL_PREFIX + '/sign-in/',
    r'^' + URL_PREFIX + '/sign-in/check-email/',
    r'^' + URL_PREFIX + '/email-resent/',
    r'^' + URL_PREFIX + '/sign-in/new-application/',
    r'^' + URL_PREFIX + '/new-application/',
    r'^' + URL_PREFIX + '/new-application/check-email/',
    r'^' + URL_PREFIX + '/service-unavailable/',
    r'^' + URL_PREFIX + '/help-contacts/',
    r'^' + URL_PREFIX + '/costs/',
    r'^' + URL_PREFIX + '/application-saved/$',
    r'^' + URL_PREFIX + '/application-cancelled/$',
    r'^' + URL_PREFIX + '/resend-code/',
    r'^' + URL_PREFIX + '/phone-number/',
)

# Regex Validation Strings
REGEX = {
    "EMAIL": "^([a-zA-Z0-9_\-\.']+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
    "MOBILE": "^(\+44|0044|0)[7][0-9]{3,14}$",
    "PHONE": "^(?:(?:\(?(?:0(?:0|11)\)?[\s-]?\(?|\+)44\)?[\s-]?(?:\(?0\)?[\s-]?)?)|(?:\(?0))(?:(?:\d{5}\)?[\s-]?\d{4,"
             "5})|(?:\d{4}\)?[\s-]?(?:\d{5}|\d{3}[\s-]?\d{3}))|(?:\d{3}\)?[\s-]?\d{3}[\s-]?\d{3,4})|(?:\d{2}\)?["
             "\s-]?\d{4}[\s-]?\d{4}))(?:[\s-]?(?:x|ext\.?|\#)\d{3,4})?$",
    "INTERNATIONAL_PHONE": "^(\+|[0-9])[0-9]{5,20}$",
    "POSTCODE_UPPERCASE": "^[A-Z]{1,2}[0-9]{1,2}[A-Z]?[0-9][A-Z][A-Z]$",
    "LAST_NAME": "^[A-zÀ-ÿ- ']+$",
    "MIDDLE_NAME": "^[A-zÀ-ÿ- ']+$",
    "FIRST_NAME": "^[A-zÀ-ÿ- ']+$",
    "TOWN": "^[A-Za-z- ]+$",
    "COUNTY": "^[A-Za-z- ]+$",
    "COUNTRY": "^[A-Za-z- ]+$",
    "VISA": "^4[0-9]{12}(?:[0-9]{3})?$",
    "MASTERCARD": "^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$",
    "MAESTRO": "^(?:5[0678]\d\d|6304|6390|67\d\d)\d{8,15}$",
    "CARD_SECURITY_NUMBER": "^[0-9]{3,4}$"
}
