# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('contrib.avatar.views',
    url('^change/$', 'change', name='avatar_change'),
)
