# -*- coding: utf-8 -*-
import os
from time import time
from random import randint
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from attachment.config import ATTACHMENT_STORAGE_DIR


def get_file_suffix(filename):
    idx = filename.rfind('.')
    return filename[idx+1:]

def upload_attachment_file_path(instance, filename):
    instance.org_filename = get_filename(filename)
    suffix = get_file_suffix(filename)
    t = str(time()).replace('.', '_')
    r = randint(1, 1000)
    fn = '%s_%s.%s' % (t, r, suffix)
    return os.path.join(ATTACHMENT_STORAGE_DIR, fn)

def get_filename(filename):
    """remove path"""
    def lt(f, x):
        f = f.split(x)
        f = f[len(f)-1]
        return f
    return lt(lt(filename, '\\'), '/')


class Attachment(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Attachment Owner'))
    attachment = models.FileField(max_length=255,
        upload_to=upload_attachment_file_path)
    original_filename = models.TextField(default='')
    description = models.TextField(default='file description', blank=True)
    activated = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s|%s' % (self.user.username, self.original_filename)
