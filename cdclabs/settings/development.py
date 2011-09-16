# -*- coding: utf-8 -*-
from os.path import join
from .common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'reversion.middleware.RevisionMiddleware',
)
INSTALLED_APPS += (
    'south',
    'debug_toolbar',
    #'reversion',
    'mercury',
)

# Development Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_PATH, '../data/openlabs'),
        'OPTIONS': {
            'timeout': 10,
        }
    }
}
INTERNAL_IPS = ('127.0.0.1',)

# Enable for mercury, instead of default tiny_mce
FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_mercury.html'
# clean html from richeditor
FEINCMS_TIDY_HTML = True
FEINCMS_TIDY_FUNCTION = 'mercury.utils.tidy'
