# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect


def register(cls, admin_cls):
    cls.add_to_class(
        'auth',
        models.BooleanField(
            _('log in to view pages'),
        )
    )

    admin_cls.fieldsets.append((_('Auth'), {
        'fields': ('auth',),
        'classes': ('collapse',),
        })
    )
