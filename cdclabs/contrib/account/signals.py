# -*- coding: utf-8 -*-
from django.contrib import auth
from django.dispatch import Signal
from django.contrib.sites.models import Site
from urlauth.signals import authkey_processed
from urlauth.models import AuthKey
from contrib.account.util import email_template


account_created = Signal(providing_args=['user', 'request'])

def authkey_handler(key, user, **kwargs):
    extra = key.extra
    action = extra.get('action')

    if 'activation' == action:
        if not user.is_active:
            user.is_active = True
            user.save()
            email_template(user.email, 'account/mail/welcome',
                user=user, domain=Site.objects.get_current().domain)

    if user.is_active:
        if 'new_email' == action:
            if 'email' in extra:
                user.email = extra['email']
                user.save()

authkey_processed.connect(authkey_handler, sender=AuthKey)
