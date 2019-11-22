from .settings import *
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'formatmodelo',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PASSWORD': '6Vlgpcr/zaira',
        'PORT': 5432
    }
}
