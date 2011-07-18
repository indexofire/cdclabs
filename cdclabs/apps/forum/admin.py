# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from forum.models import *


def update_topic_num_replies(modeladmin, request, queryset):
    for topic in queryset:
        topic.num_replies = topic.count_nums_replies()
        topic.save()
update_topic_num_replies.short_description = _(u"Update replies numbers")

def update_forum_nums_topic_post(modeladmin, request, queryset):
    for forum in queryset:
        forum.num_topics = forum.count_nums_topic()
        forum.num_posts = forum.count_nums_post()
        if forum.num_topics:
            forum.last_post = forum.topic_set.order_by('-last_reply_on')[0].last_post
        else:
            forum.last_post = ''
        forum.save()
update_forum_nums_topic_post.short_description = _(u"Update topic/post numbers")

class ForumAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'slug', 
        'category', 
        'num_topics',
        'num_posts',
    )
    list_filter = ('category',)
    actions = [update_forum_nums_topic_post]

class PostInline(admin.TabularInline):
    model = Post

class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'subject', 
        'forum', 
        'posted_by', 
        'sticky', 
        'closed', 
        'hidden', 
        'num_views', 
        'num_replies', 
        'created_on', 
        'updated_on', 
    )
    list_filter = ('forum', 'sticky', 'closed', 'hidden',)
    search_fields = ('subject', 'posted_by__username', )
    inlines = (PostInline, )
    actions = [update_topic_num_replies]

class PostAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 
        'topic', 
        'posted_by', 
        'poster_ip',
        'created_on', 
        'updated_on', 
    )
    search_fields = ('topic__subject', 'posted_by__username', 'message', )

class ForumUserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'userrank', 
        'last_activity', 
        'last_posttime',
        'signature',
    )
    search_fields = ('user', 'userrank', )

admin.site.register(ForumCategory)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ForumUserProfile, ForumUserProfileAdmin)
