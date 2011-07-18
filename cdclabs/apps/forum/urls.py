# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from forum.views import *

urlpatterns = patterns('',
    url(r'^$', index, name='forum_index'),
    url(r'^forum/(?P<forum_slug>\w+)/$', forum, name='forum_forum'),
    url(r'^topic/(?P<topic_id>\d+)/$', topic, name='forum_topic'),
    url(r'^topic/new/(?P<forum_id>\d+)/$', new_post, name='forum_new_topic'),
    url(r'^reply/new/(?P<topic_id>\d+)/$', new_post, name='forum_new_replay'),
    url(r'^post/(?P<post_id>\d+)/$', post, name='forum_post'),
    url(r'^post/(?P<post_id>\d+)/edit/$', edit_post, name='forum_post_edit'),
    url(r'^user/(?P<user_id>\d+)/topics/$', user_topics,
        name='forum_user_topics'),
    url(r'^user/(?P<user_id>\d+)/posts/$', user_posts,
        name='forum_user_posts'),
    url('^markitup_preview/$', markitup_preview, name='markitup_preview'),
)
