# -*- coding: utf-8 -*-
from django.conf import settings


DEFAULT_CTX_CONFIG = {
    'FORUM_TITLE': '',
    'FORUM_SUB_TITLE': '',
    'FORUM_PAGE_SIZE': 50,
    'TOPIC_PAGE_SIZE': 20,
}

CTX_CONFIG = getattr(settings, 'FORUM_CTX_CONFIG', DEFAULT_CTX_CONFIG)
