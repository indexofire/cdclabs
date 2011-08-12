# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _


def create_perm():
    pass

def register(cls, admin_cls):
    cls.add_to_class('auth',
        models.BooleanField(_('auth checkbox'),
        help_text = _('if need logging to view pages'),
        default=False),
        )
    """
    cls.add_to_class('user',
        models.ForeignKey(User),
        )
    cls.add_to_class('group',
        models.ForeignKey(Group),
        )
    """
    admin_cls.fieldsets.append(
        (_('Auth'),{
            'fields': ('auth',),
            'classes': ('collapse',),
        })
    )
