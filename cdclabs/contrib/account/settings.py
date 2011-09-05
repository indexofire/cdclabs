# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


# account model and form
USER_MODEL = getattr(settings, 'ACCOUNT_USER_MODEL',
    'django.contrib.auth.models.User')
LOGIN_FORM = getattr(settings, 'ACCOUNT_LOGIN_FORM',
    'contrib.account.forms.LoginForm')

# account registration
REGISTRATION_REDIRECT_URLNAME = getattr(settings,
    'ACCOUNT_REGISTRATION_REDIRECT_URLNAME', 'registration_complete')
REGISTRATION_FORM = getattr(settings,
    'ACCOUNT_REGISTRATION_FORM', 'contrib.account.forms.RegistrationForm')
REGISTRATION_ENABLED = getattr(settings, 'ACCOUNT_REGISTRATION_ENABLED', True)
ACTIVATION_REQUIRED = getattr(settings, 'ACCOUNT_ACTIVATION_REQUIRED', True)
AUTHENTICATION_WITH_EMAIL = getattr(settings,
    'ACCOUNT_AUTHENTICATION_WITH_EMAIL', False)

# account password
PASSWORD_RESET_FORM = getattr(settings, 'ACCOUNT_PASSWORD_RESET_FORM',
    'account.forms.PasswordResetForm')
PASSWORD_CHANGE_FORM = getattr(settings, 'ACCOUNT_PASSWORD_CHANGE_FORM',
    'account.forms.PasswordChangeForm')
PASSWORD_CHANGE_REQUIRES_OLD = getattr(settings,
    'ACCOUNT_PASSWORD_CHANGE_REQUIRES_OLD', True)

# account captcha
CAPTCHA_ENABLED = getattr(settings, 'ACCOUNT_CAPTCHA_ENABLED', False)
CAPTCHA_FIELD = getattr(settings, 'ACCOUNT_CAPTCHA_FIELD',
    'captcha.fields.CaptchaField')
CAPTCHA_LABEL = getattr(settings, 'ACCOUNT_CAPTCHA_LABEL',
    _('Enter the text on the image'))
