# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from forum.models import Topic, Post


def gen_last_post_info(post):
    last_post = {'posted_by': post.posted_by.username,
        'update': post.created_on}
    return b64encode(pickle.dumps(last_post, pickle.HIGHEST_PROTOCOL))

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ForumUserProfile.objects.create(user=instance)

def update_topic_on_post(sender, instance, created, **kwargs):
    if created:
        instance.topic.last_post = gen_last_post_info(instance)
        instance.topic.last_reply_on = instance.created_on
        instance.topic.num_replies += 1
        instance.topic.save()

def update_forum_on_post(sender, instance, created, **kwargs):
    if created:
        instance.topic.forum.last_post = gen_last_post_info(instance)
        instance.topic.forum.num_posts += 1
        instance.topic.forum.save()

def update_forum_on_topic(sender, instance, created, **kwargs):
    if created:
        instance.forum.num_topics += 1
        instance.forum.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(update_topic_on_post, sender=Post)
post_save.connect(update_forum_on_post, sender=Post)
post_save.connect(update_forum_on_topic, sender=Topic)
