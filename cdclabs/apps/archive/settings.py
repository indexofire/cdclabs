# -*- coding: utf-8 -*-
from django.conf import settings


MULTIPLE_PROFILES = getattr(settings, 'AUTH_PROFILE_MODULE', None)
PROFILE_BASE = getattr(settings,
DEFAULT_PROFILE_MODULE = getattr(settings,
