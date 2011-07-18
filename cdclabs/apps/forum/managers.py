# -*- coding: utf-8 -*-
from django.db import models


class TopicManager(models.Manager):
    def get_query_set(self):
        return super(TopicManager, self).get_query_set().filter(hidden=False)
