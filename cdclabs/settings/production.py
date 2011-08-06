# -*- coding: utf-8 -*-
from os.path import join
from .common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    'gunicorn',
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
