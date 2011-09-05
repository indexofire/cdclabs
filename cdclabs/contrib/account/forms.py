# -*- coding: utf-8
import re
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from django.template import loader
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from .util import load_class
from .settings import *


UserModel = load_class(USER_MODEL)

if CAPTCHA_ENABLED:
    CaptchaField = load_class(CAPTCHA_FIELD)

RE_USERNAME = getattr(settings, 'ACCOUNT_RE_USERNAME',
    re.compile(r'[a-z0-9][_a-z0-9]*[a-z0-9]$', re.I))
USERNAME_MIN_LENGTH = getattr(settings, 'ACCOUNT_USERNAME_MIN_LENGTH', 3)
USERNAME_MAX_LENGTH = getattr(settings, 'ACCOUNT_USERNAME_MAX_LENGTH', 20)
PASSWORD_MIN_LENGTH = getattr(settings, 'ACCOUNT_PASSWORD_MIN_LENGTH', 3)
PASSWORD_MAX_LENGTH = getattr(settings, 'ACCOUNT_PASSWORD_MAX_LENGTH', 15)


class PasswordField(forms.CharField):
    """
    Form field for password handling.
    """
    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(*args, **kwargs)
        self.widget = forms.PasswordInput(render_value=False)
        self.help_text = ''

    def clean(self, value):
        super(PasswordField, self).clean(value)
        if len(value) < PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(_(u'Password length is less than %(min)d') % {'min': PASSWORD_MIN_LENGTH})
        if len(value) > PASSWORD_MAX_LENGTH:
            raise forms.ValidationError(_(u'Password length is more than %(max)d') % {'max': PASSWORD_MAX_LENGTH})
        return value


class RegistrationForm(forms.Form):
    username = forms.CharField(label=_(u'Login'), help_text=_(u'You can use a-z, 0-9 and underscore. Login length could be from %(min)s to %(max)s chars.') % {'min': USERNAME_MIN_LENGTH, 'max': USERNAME_MAX_LENGTH})
    email = forms.EmailField(label=_('Email'))
    password = PasswordField(label=_('Password'))
    password_dup = PasswordField(label=_('Password (confirmation)'))

    default_error_messages = {
        'short_login': _(u'Login length is less than %(min)d'),
        'long_login': _(u'Login length is more than %(max)d'),
        'invalid_login': _(u'Login contains restricted symbols'),
        'taken_login': _(u'This login already registered'),
        'taken_email': _(u'This email already registered.'),
        'mismatched_passwords': _('Passwords do not match'),
    }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if settings.ACCOUNT_CAPTCHA_ENABLED:
            self.fields['captcha'] = CaptchaField(label=settings.ACCOUNT_CAPTCHA_LABEL)

    def clean_username(self):
        if 'username' in self.cleaned_data:
            value = self.cleaned_data['username']
            if len(value) < USERNAME_MIN_LENGTH:
                raise forms.ValidationError(self.default_error_messages['short_login'] % {'min': USERNAME_MIN_LENGTH})
            if len(value) > USERNAME_MAX_LENGTH:
                raise forms.ValidationError(self.default_error_messages['long_login'] % {'max': USERNAME_MAX_LENGTH})
            if not RE_USERNAME.match(value):
                raise forms.ValidationError(self.default_error_messages['invalid_login'])

            try:
                UserModel.objects.get(username__exact=value)
            except UserModel.DoesNotExist:
                return value
            else:
                raise forms.ValidationError(self.default_error_messages['taken_login'])

    def clean_email(self):
        #return self.cleaned_data.get('email','')
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                UserModel.objects.get(email__exact=email)
            except UserModel.DoesNotExist:
                return email
            else:
                raise forms.ValidationError(self.default_error_messages['taken_email'])


    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password_dup')
        if pwd1 and pwd2:
            if pwd1 != pwd2:
                # show error on top of password_dup field
                self._errors['password_dup'] = [self.default_error_messages['mismatched_passwords']]
        return self.cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = UserModel.objects.create_user(username, email, password)
        if settings.ACCOUNT_ACTIVATION_REQUIRED:
            user.is_active = False
            user.save()
        return user


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    default_error_messages = {'taken_email': _(u'This email is not registered')}

    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            if UserModel.objects.filter(email=email).count():
                return email
            else:
                raise forms.ValidationError(self.default_error_messages['taken_email'])


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    default_error_messages = {
        'invalid_account': _(u'Incorrect login or password'),
        'inactive_account': _(u'Sorry. You account is not active. Maybe you didn\'t activate it.'),
    }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.base_fields['username'].help_text = ''
        #self.base_fields['password'].widget = forms.PasswordInput()
        self.base_fields['password'].help_text = ''
        super(LoginForm, self).__init__(*args, **kwargs)


    def clean(self):
        super(LoginForm, self).clean()
        if self.is_valid():
            user = authenticate(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'])
            if not user is None:
                if user.is_active:
                    login(self.request, user)
                    return self.cleaned_data
                else:
                    raise forms.ValidationError(self.default_error_messages['inactive_account'])
            else:
                raise forms.ValidationError(self.default_error_messages['invalid_account'])


# TODO: REWRITE THIS HELL HORROR

class PasswordChangeForm(forms.Form):
    """
    Form for changing user's password.
    """

    old_password = PasswordField(label=_(u'Old password'))
    password = PasswordField(label=_(u'Password'))
    password_confirmation = PasswordField(label=_(u'Password (confirmation)'))
    authkey = forms.CharField(widget=forms.HiddenInput, required=False)
    uid = forms.CharField(widget=forms.HiddenInput, required=False)

    default_error_messages = {
        'invalid_password': _('Incorrect old password'),
        'mismatched_passwords': _(u'The passwords do not match'),
    }

    def __init__(self, *args, **kwargs):
        self.require_old = kwargs.pop('require_old', True)
        self.user = kwargs.pop('user')
        if not self.require_old:
            self.base_fields['old_password'] = forms.Field(widget=forms.HiddenInput, required=False)
        super(PasswordChangeForm, self).__init__(*args, **kwargs)


    def clean(self):
        if 'old_password' in self.cleaned_data and 'uid' in self.cleaned_data:
            password = self.cleaned_data['old_password']
            uid = self.cleaned_data['uid']
            if password:
                test_user = authenticate(username=self.user.username, password=password)
                if not test_user:
                    del self.cleaned_data['old_password']
                    self._errors['old_password'] = [self.default_error_messages['invalid_password']]
        return self.cleaned_data


    def clean_password_confirmation(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password_confirmation']
        if pass1 != pass2:
            raise forms.ValidationError(self.default_error_messages['mismatched_passwords'])
        else:
            return pass1


    def clean_uid(self):
        if self.require_old:
            return self.cleaned_data['uid']
        else:
            try:
                user = User.objects.get(pk=self.cleaned_data['uid'])
                self.user = user
                return self.cleaned_data['uid']
            except User.DoesNotExist:
                raise forms.ValidationError(_(u'Invalid username'))


    def save(self):
        self.user.set_password(self.cleaned_data['password'])
        self.user.save()
        return self.user


class EmailChangeForm(forms.Form):
    """
    Form for email chanage.
    """

    email = forms.EmailField(label=_(u'New email'))
