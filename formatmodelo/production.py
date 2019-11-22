from .settings import *
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['formatmodelo.herokuapp.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dfnudhma0i23h0',
        'HOST': 'ec2-174-129-227-80.compute-1.amazonaws.com',
        'USER': 'ebvkkbqeeleizq',
        'PASSWORD': '309f259a1466abab39aa5cbe48a348544bd04e7e86f96326cd8d358b43efac8a',
        'PORT': 5432,
    }
}