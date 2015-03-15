"""
Django settings for SMSSchedulerServer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from getenv import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', '9b9%5fwgtj2vaabqlkkk+n4h93-&@d3e5&6+k#c(&4wkjjn9m*')

EMAIL_SALT = env("EMAIL_SALT", 'O3uZZB9Jtre30N4hqQlNOlQQag9t/gK6o66myeMfpKY=')
EMAIL_KEY = env("EMAIL_KEY", 'F9zP2mHyuSK0G1Tz8MXsKALrgqu4g6qL65XOdWKJvtM=')

AUTH_USER_MODEL = 'accounts.User'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: don't run with TEST MODE turned on in production!
if DEBUG:
    TEST_MODE = True
else:
    TEST_MODE = env('TEST_MODE', False)

if DEBUG:
    ENV_NAME = "dev"
elif TEST_MODE:
    ENV_NAME = "test"
else:
    ENV_NAME = "production"

ALLOWED_HOSTS = env('ALLOWED_HOSTS', '').split()

#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'oauth2_provider',
    'crispy_forms',

    'accounts',
    'api',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SMSSchedulerServer.urls'

WSGI_APPLICATION = 'SMSSchedulerServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DBNAME', 'SMSSchedulerServer_dev'),
        'HOST': env('DBHOST', None),
        'USER': env('DBUSER', None),
        'PASSWORD': env('DBPASS', None),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Bug tracking
BUGSNAG_NOTIFY = env('BUGSNAG_NOTIFY', False)
MIDDLEWARE_CLASSES.append("bugsnag.django.middleware.BugsnagMiddleware")
BUGSNAG = {
    "api_key": "",
    "project_root": BASE_DIR,
    "release_stage": ENV_NAME,
    "auto_notify": BUGSNAG_NOTIFY,
    "notify_release_stages": ["production", "test"],
}

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read_profile': 'Access your user profile.',
        'update_profile': 'Update your user profile.',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = env('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Crispy Forms Template Pack: bootstrap | bootstrap3 | uni-form | foundation
# http://django-crispy-forms.readthedocs.org/en/latest/
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Nose Tests
# https://pypi.python.org/pypi/django-nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Django REST Framework
# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    )
}
