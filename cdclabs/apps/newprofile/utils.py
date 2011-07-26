# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import get_model
from django.contrib.auth.models import SiteProfileNotAvailable


def get_profile_model():
    """
    Return the model class name for the currently-active user profile
    model, as defined by the ``AUTH_PROFILE_MODULE`` setting. If that
    settings is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    """
    if (not hasattr(settings, 'AUTH_PROFILE_MODEL')) or (not settings.AUTH_PROFILE_MODEL):
        raise SiteProfileNotAvailable

    profile_model = get_model(*settings.AUTH_PROFILE_MODEL.split('.'))
    if profile_model is None:
        raise SiteProfileNotAvailable
    return profile_model

def get_profile_form():
    """
    Return a form which is suitable for creating or editing instances
    of the site-specific user profile model. The definition is in
    settings ``AUTH_PROFILE_MODULE``. If the variable is missing, raise
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    """
    profile_model = get_profile_model()
    class _ProfileForm(forms):
        class Meta:
            model = profile_model
            exclude = ('user',)

    return _ProfileForm
