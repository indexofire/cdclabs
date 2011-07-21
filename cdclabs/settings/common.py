# -*- coding: utf-8 -*-
import sys
from os.path import (
    dirname,
    abspath,
    normpath,
    basename,
    join,
)


# Project Path
PROJECT_PATH = normpath(dirname(dirname(abspath(__file__))))
PROJECT_NAME = basename(PROJECT_PATH)

# Add sys.path
sys.path.append(join(PROJECT_PATH, 'apps'))
sys.path.append(join(PROJECT_PATH, 'contrib'))

# Admin
ADMINS = (
    ('administrator', 'admin@localhost.com'),
)
MANAGERS = ADMINS

# Localize
TIME_ZONE     = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'
SITE_ID       = 1
USE_I18N      = True
USE_L10N      = True
LANGUAGES     = (
    ('zh-cn', 'Simplified Chinese'),
    ('en-us', 'English'),
)

# Static File
MEDIA_ROOT  = join(PROJECT_PATH, 'media')
STATIC_ROOT = join(PROJECT_PATH, 'statics')
MEDIA_URL   = '/media/'
STATIC_URL  = '/static/'
TINYMCE_JS_URL      = '/libs/tiny_mce/tiny_mce.js'
ADMIN_MEDIA_PREFIX  = '/static/admin/'
#STATICFILES_DIRS    = (
#    join(PROJECT_PATH, 'assets'),
#)

# Static Files Finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Templates Loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

# APP
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    'feincms',
    'feincms.module.page',
    #'feincms_ext.content_type.highcharts',
    #'paging',
    #'indexer',
    'apps.base',
    #'apps.emboss',
    #'apps.forum',
    #'apps.attachment',
    'contrib.account',
    #'apps.group',
    #'apps.profile',
    'contrib.content.googlemaps',
    'contrib.content.markup',
    'contrib.form_designer',
)


ROOT_URLCONF = '%s.urls' % PROJECT_NAME

#SECRET_FILE = normpath(join(SITE_ROOT, 'deploy', 'SECRET'))
SECRET_KEY = 'r4@l+cguic(r5)rojtu*+txbwz7*v1_k-u_uxukl9tqvu600oq'
"""
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        with open(SECRET_FILE, 'w') as f:
            f.write(gen_secret_key(50))
    except IOError:
    raise Exception('Cannot open file `%s` for writing.' % SECRET_FILE)
"""

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

# Templates Files
TEMPLATE_DIRS = (
    join(PROJECT_PATH, 'templates'),
)

MARKUP_CODE_HIGHTLIGHT = True

from contrib.account.settings import *
