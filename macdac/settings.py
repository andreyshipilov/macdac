# -*- coding: utf-8 -*-
import sys
from os.path import join, abspath, dirname



PROJECT_DIR = dirname(__file__)

# Paths to add on os.path
PATHS = (
    abspath(join(PROJECT_DIR, 'apps')),
)
[sys.path.insert(0, i) if i not in sys.path else None for i in PATHS]

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Andrey Shipilov', 'a@andreyshipilov.com'),
)
MANAGERS = ADMINS

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
SITE_ID = 1
USE_L10N = True

MEDIA_ROOT = join(PROJECT_DIR, 'static/media')
MEDIA_URL = '/media/'
STATIC_ROOT = join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'macdac.urls'

WSGI_APPLICATION = 'macdac.wsgi.application'

TEMPLATE_DIRS = (
    join(PROJECT_DIR, 'templates'),
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'news.context_processor.update_context',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'news',

    'pagination',
    'robots',
    'south',
    'debug_toolbar',
    'compressor',
    'google_analytics',
    'sorl.thumbnail',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Debug Toolbar and shit
INTERNAL_IPS = ('127.0.0.1',)

# Compressor
COMPRESS_OUTPUT_DIR = 'min'
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter',]

# Pagination
PAGINATION_DEFAULT_PAGINATION = 10
PAGINATION_DEFAULT_WINDOW = 2


# Local settings
try:
    from local_settings import *
except ImportError:
    pass

# Live settings
try:
    from live_settings import *
except ImportError:
    pass
