# Django settings for dogwalk project.
import os
import sys
import json

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

STATIC_ROOT = os.path.join(PROJECT_PATH, '../staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': '', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dogwalk',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
USE_TZ = False
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')-rbjy9n*dybxz)^lf5tk_cdgm)j17%q2a+46x-f3o8vmn0%03'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', #FIXTHIS
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dogwalk.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dogwalk.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, '../templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'fixture_magic',
    'south',
    'dogwalk',
    'dog',
    'graph',
    'schedule'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'MA': {
            'format': '%(levelname)s\t%(time).16s\t%(walker).6s\t%(node).12s\t%(carrying).80s\t%(message)s'
        },
        'MS': {
            'format': '%(message)s'
        },
        'MV': {
            'format': '%(levelname)s\t%(start).16s\t%(end).16s\t\t%(dog).6s\t%(days)d\t%(events)d\t%(cancellations)s\t%(message)s'
        }
    },
    'handlers': {
        'MA': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'MA.log',
            'formatter': 'MA'
            },
        'MS': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'MS.log',
            'formatter': 'MS'
        },
        'MV': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'MV.log',
            'formatter': 'MV'
        }
    },
    'loggers': {
        'MA': {
            'handlers': ['MA'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'MS': {
            'handlers': ['MS'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'MV': {
            'handlers': ['MV'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Parse database configuration from $DATABASE_URL
db = {'username': 'postgres',
      'password': 'beffy44',
      'name': 'dogwalk',}

import dj_database_url
DATABASES['default'] = dj_database_url.config(
                        default='postgres://%s:%s@localhost:5432/%s' % (
                                db['username'], 
                                db['password'], 
                                db['name'])
                        )

#if 'test' in sys.argv:
#    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'ignoretests.DjangoIgnoreTestSuiteRunner'

IGNORE_TESTS = (
    'django_extensions',
)


