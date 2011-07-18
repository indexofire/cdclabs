# -*- coding: utf-8 -*-
from django.conf import settings


ATTACHMENT_STORAGE_DIR = getattr(settings, 'ATTACHMENT_STORAGE_DIR',
    '%sattachment' % settings.MEDIA_ROOT)
