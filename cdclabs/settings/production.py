# -*- coding: utf-8 -*-
from os.path import join
from .common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG
GOOGLE_ANALYTICS = True
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

# Production Database
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hzcdclabs',
        'USER': 'django_cdc',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
"""
