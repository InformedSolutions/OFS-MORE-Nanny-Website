from .base import *

INSTALLED_APPS = BUILTIN_APPS + THIRD_PARTY_APPS + PROD_APPS + PROJECT_APPS

SECRET_KEY = os.environ.get('SECRET_KEY', '!cpk9yyix!m9(jgc7ufreu-il0nj)p@w!l)g4cg@g8#-c9uq-p')
