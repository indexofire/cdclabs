# -*- coding: utf-8 -*-
from django.conf import settings
from forum.settings import CTX_CONFIG


def page_size(request):
    if hasattr(settings, 'FORUM_CTX_CONFIG'):
        context = settings.FORUM_CTX_CONFIG
    return context
