# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from urlauth.util import wrap_url
from contrib.account import signals
from contrib.account.forms import PasswordResetForm, PasswordChangeForm, LoginForm, EmailChangeForm
from contrib.account.util import email_template, build_redirect_url, load_class
from .settings import *
from utils.views.helper import render_to


RegistrationForm = load_class(REGISTRATION_FORM)
LoginForm = load_class(LOGIN_FORM)
PasswordResetForm = load_class(PASSWORD_RESET_FORM)
ChangePasswordForm = load_class(PASSWORD_CHANGE_FORM)
UserModel = load_class(USER_MODEL)
hostname = Site.objects.get_current().domain

@render_to('account/message.html')
def message(request, msg):
    """
    Shortcut that prepare data for message view.
    """
    return {'message': msg,}

@render_to('account/registration.html')
def registration(request, form_class=RegistrationForm):
    if not REGISTRATION_ENABLED:
        return message(request, _('Sorry. Registration is disabled.'))
    if request.user.is_authenticated():
        return message(request, _('You have to logout before registration'))

    if 'POST' == request.method:
        form = form_class(request.POST, request.FILES)
    else:
        form = form_class()

    if form.is_valid():
        user = form.save()

        signals.account_created.send(None, user=user, request=request)
        password = form.cleaned_data['password']

        if ACTIVATION_REQUIRED:
            url = 'http://%s%s' % (hostname, reverse('registration_complete'))
            url = wrap_url(url, uid=user.id, action='activation')
            params = {'domain': hostname, 'login': user.username, 'url': url, 'password': password}
            if email_template(user.email, 'account/mail/activation_required',
                **params):
                return HttpResponseRedirect(reverse('activation_required'))
            else:
                user.delete()
                return message(request, _('''The error was occuried while
                    sending email with activation code. Account was not
                    created. Please, try later.'''))
        else:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            args = {'domain': hostname, 'user': user, 'password': password}
            email_template(user.email, 'account/mail/registration_complete',
                **args)
            return redirect(reverse(REGISTRATION_REDIRECT_URLNAME))

    return {'form': form,}

@render_to('account/password_reset.html')
def password_reset(request, form_class=PasswordResetForm):
    if 'POST' == request.method:
        form = form_class(request.POST)
    else:
        form = form_class()

    if form.is_valid():
        user = UserModel.objects.get(email=form.cleaned_data['email'])
        url = 'http://%s%s' % (hostname, reverse('auth_password_change'))
        url = wrap_url(url, uid=user.id, onetime=False,
            action='password_change')
        args = {'domain': hostname, 'url': url, 'user': user}
        if email_template(user.email, 'account/mail/password_reset', **args):
            return message(request, _('Check the mail please'))
        else:
            return message(request, _('''Unfortunately we could not send you
                email in current time. Please, try later'''))

    return {'form': form,}

@render_to('account/login.html')
def login(request, form_class=LoginForm):
    """
    Wrap login action
    """
    if request.user.is_authenticated():
        return message(request, _('You are already authenticated'))

    if request.method == 'POST':
        form = form_class(request.POST, request=request)
    else:
        form = form_class(request=request)

    request.session['login_redirect_url'] = request.GET.get('next')
    if form.is_valid():
        redirect_url = build_redirect_url(request, settings.LOGIN_REDIRECT_URL)
        return HttpResponseRedirect(redirect_url)
    return {'form': form,}

@render_to('account/password_change.html')
def password_change(request):
    """
    That view is used in two cases:
     * User is authenticated. He fills the from with old password new one.
     * User follow the link from reset password email. In that case field for
       old password is invisible.
    """

    authkey = None
    if hasattr(request, 'authkey'):
        if request.authkey.extra.get('action') == 'password_change':
            authkey = request.authkey

    if not request.user.is_authenticated():
        if not authkey:
            return HttpResponseRedirect(reverse('auth_login') + '?next=%s' % request.path)

    if authkey:
        require_old = False
        initial = {'authkey': authkey.id, 'uid': authkey.uid}
    else:
        require_old = True
        initial = {}

    if 'POST' == request.method:
        form = ChangePasswordForm(request.POST, require_old=require_old,
            user=request.user)
    else:
        form = ChangePasswordForm(require_old=require_old, initial=initial,
            user=request.user)
    if form.is_valid():
        form.save()
        if authkey:
            authkey.delete()
        return HttpResponseRedirect(reverse('auth_password_change_done'))
    return {'form': form,}

@login_required
@render_to('account/email_change.html')
def email_change(request):
    if 'POST' == request.method:
        form = EmailChangeForm(request.POST)
    else:
        form = EmailChangeForm()

    if form.is_valid():
        email = form.cleaned_data['email']
        url = 'http://%s%s' % (hostname, reverse('auth_email_change_done'))
        url = wrap_url(url, uid=request.user.id, action='new_email', email=email)
        args = {'domain': hostname, 'url': url, 'email': email,}
        if email_template(email, 'account/mail/email_change', **args):
            return message(request, _('Check the mail please'))
        else:
            return message(request, _('Unfortunately we could not send you email in current time. Please, try later'))
    return {'form': form,}

@login_required
def email_change_done(request):
    return message(request, _('Your email has been changed to %s') % request.user.email)

@render_to('account/password_change_done.html')
def password_change_done(request):
    return {'login_url': reverse('auth_login'),}

def logout(request):
    auth.logout(request)
    next = request.GET.get('next', reverse('auth_logout_successful'))
    return HttpResponseRedirect(next)

def logout_successful(request):
    return message(request, _('You have successfully loged out'))
