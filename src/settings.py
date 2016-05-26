from djangoappengine.settings_base import *
has_djangoappengine = True

import dbindexer
import os

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'djangotoolbox',
    'autoload',
    'dbindexer',

    # djangoappengine should come last
    'djangoappengine')

INSTALLED_APPS += ('corksponge',)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware')

DATABASES = {
        'default': {
                'ENGINE': 'dbindexer',
                'TARGET': 'gae',
            },
        'gae': {
                'ENGINE': 'djangoappengine.db'
            },
    }

DBINDEXER_SITECONF = 'dbindexes'

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

TEMPLATE_LOADERS = (
   'django.template.loaders.filesystem.Loader',
   'django.template.loaders.app_directories.Loader',
   'django.template.loaders.app_directories.load_template_source')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages')

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_URL = '/files/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'files')
AUTOLOAD_SITECONF = 'dbindexes'

ROOT_URLCONF = 'urls'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/user/login'
LOGOUT_URL = '/user/logout'

STATIC_URL = '/'
SITE_ID = 1

DEBUG = False

MAX_X = 4000
MAX_Y = 4000
