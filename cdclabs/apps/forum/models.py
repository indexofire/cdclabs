# -*- coding: utf-8 -*-
from base64 import b64encode, b64decode
try:
    import cPickle as pickle
except:
    import pickle
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from forum.settings import *
from forum.managers import TopicManager
from attachment.models import Attachment


__all__ = [
    'Config',
    'ForumCategory',
    'Forum',
    'ForumUserProfile',
    'Post',
    'Topic',
]

class Config(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class ForumCategory(models.Model):
    """
    Forum Category Model
    """
    name = models.CharField(max_length=100)
    description = models.TextField(default='Category Description')
    ordering = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('-ordering', 'created_on')

    def __unicode__(self):
        return self.name

class Forum(models.Model):
    """
    Forum Model
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(default='Forum Desctiption')
    ordering = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(ForumCategory)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    num_topics = models.IntegerField(default=0)
    num_posts = models.IntegerField(default=0)
    last_post = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")
        ordering = ('ordering', '-created_on')

    def count_nums_topic(self):
        return self.topic_set.all().count()

    def count_nums_post(self):
        return self.topic_set.all(). \
            aggregate(Sum('num_replies'))['num_replies__sum'] or 0

    def get_last_post(self):
        if not self.last_post:
            return {}
        return pickle.loads(b64decode(self.last_post))

    @models.permalink
    def get_absolute_url(self):
        return ('forum_forum', (), {'forum_slug': self.slug})

    def __unicode__(self):
        return self.name


class Topic(models.Model):
    forum = models.ForeignKey(Forum, verbose_name=_('Forum'))
    posted_by = models.ForeignKey(User)
    subject = models.CharField(max_length=999)
    num_views = models.IntegerField(default=0)
    num_replies = models.PositiveSmallIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    last_reply_on = models.DateTimeField(auto_now_add=True)
    last_post = models.CharField(max_length=255, blank=True)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    objects = TopicManager()

    class Meta:
        ordering = ('-last_reply_on',)
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __unicode__(self):
        return self.subject

    def count_nums_replies(self):
        return self.post_set.all().count()

    @models.permalink
    def get_absolute_url(self):
        return ('forum_topic', (), {'topic_id': self.id})

    def get_last_post(self):
        if not self.last_post:
            return {}
        return pickle.loads(b64decode(self.last_post))


class Post(models.Model):
    topic = models.ForeignKey(Topic, verbose_name=_('Topic'))
    posted_by = models.ForeignKey(User)
    poster_ip = models.IPAddressField()
    topic_post = models.BooleanField(default=False)
    message = models.TextField()
    attachments = models.ManyToManyField(Attachment, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null = True)
    edited_by = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-created_on',)
        get_latest_by = ('created_on', )

    def __unicode__(self):
        return self.message[:80]

    def subject(self):
        if self.topic_post:
            return _('Topic: %s') % self.topic.subject
        return _('Re: %s') % self.topic.subject

    def update_attachments(self, attachment_ids):
        self.attachments.clear()
        for attachment_id in attachment_ids:
            try:
                attachment = Attachment.objects.get(pk=attachment_id)
            except:
                continue
            attachment.activated = True
            attachment.save()
            self.attachments.add(attachment)

    @models.permalink
    def get_absolute_url(self):
        return ('forum_post', (), { 'post_id': self.pk })

    def get_absolute_url_ext(self):
        topic = self.topic
        post_idx = topic.post_set.filter(created_on__lte=self.created_on). \
            count()
        page = (post_idx - 1) / CTX_CONFIG['TOPIC_PAGE_SIZE'] + 1
        return '%s?page=%s#p%s' % (topic.get_absolute_url(), page, self.pk)


class ForumUserProfile(models.Model):
    user = models.OneToOneField(User, related_name='forum_profile',
        verbose_name=_('User'))
    last_activity = models.DateTimeField(auto_now_add=True)
    userrank = models.CharField(max_length=30,default="Junior Member")
    last_posttime = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length = 1000, blank = True)

    def __unicode__(self):
        return self.user.username

    def get_total_posts(self):
        return self.user.post_set.count()

    def get_absolute_url(self):
        return self.user.get_absolute_url()
