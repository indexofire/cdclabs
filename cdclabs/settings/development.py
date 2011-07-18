# -*- coding: utf-8 -*-
from os.path import join
from .common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INSTALLED_APPS += (
    'south',
    'debug_toolbar',
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
