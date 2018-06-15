from .base import *

URL_PREFIX = '/nanny'

STATIC_URL = URL_PREFIX + '/static/'

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROJECT_APPS

SECRET_KEY = os.environ.get('SECRET_KEY', '!cpk9yyix!m9(jgc7ufreu-il0nj)p@w!l)g4cg@g8#-c9uq-p')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'ofsted'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'OfstedB3ta'),
        'HOST': os.environ.get('POSTGRES_HOST', '130.130.52.132'),
        'PORT': os.environ.get('POSTGRES_PORT', '5462')
    }
}

MIGRATION_MODULES = {
    'login_app': 'login_app.tests.test_migrations',
    'tasks_app': 'tasks_app.tests.test_migrations'
}
