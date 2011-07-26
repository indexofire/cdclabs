# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _


ACCOUNT_USER_MODEL = 'django.contrib.auth.models.User'
ACCOUNT_LOGIN_FORM = 'account.forms.LoginForm'

ACCOUNT_REGISTRATION_REDIRECT_URLNAME = 'registration_complete'
ACCOUNT_REGISTRATION_FORM = 'account.forms.RegistrationForm'
ACCOUNT_REGISTRATION_ENABLED = True
ACCOUNT_ACTIVATION_REQUIRED = True
ACCOUNT_AUTHENTICATION_WITH_EMAIL = False

ACCOUNT_PASSWORD_RESET_FORM = 'account.forms.PasswordResetForm'
ACCOUNT_PASSWORD_CHANGE_FORM = 'account.forms.PasswordChangeForm'
ACCOUNT_PASSWORD_CHANGE_REQUIRES_OLD = True

ACCOUNT_CAPTCHA_ENABLED = False
ACCOUNT_CAPTCHA_FIELD = 'captcha.fields.CaptchaField'
ACCOUNT_CAPTCHA_LABEL = _('Enter the text on the image')
