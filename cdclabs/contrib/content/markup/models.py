# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.conf import settings
from django.template import TemplateSyntaxError, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from .forms import MarkupContentAdminForm
from .utils import MarkupParser


class MarkupContent(models.Model):
    """
    Markup content type models
    """
    MARKUP_CHOICES = (
        ('rst', 'RestructuredText'),
        ('markdown', 'Markdown'),
        ('textile', 'Textile')
    )
    markup = models.TextField(_("Markup Text"), blank=False)
    markup_type = models.CharField(max_length=20, blank=False,
        choices=MARKUP_CHOICES)
    markup_html = models.TextField(blank=False)
    template = 'markup/default.html'
    feincms_item_editor_form = MarkupContentAdminForm
    #feincms_item_editor_context_processors = (
    #    lambda x: dict(MARKITUP_JS_URL = settings.MARKITUP_JS_URL),
    #)
    feincms_item_editor_includes = {'head': [ 'markup/init.html',],}

    class Meta:
        abstract = True
        verbose_name = _('Markup')
        verbose_name_plural = _('Markup')

    @property
    def media(self):
        return forms.Media(css={'all': ('markup/css/markup.css',)}, js=())

    def save(self, *args, **kwargs):
        #self.markup_html = {'rst': lambda x: restructuredtext(x),
        #    'markdown': lambda x: markdown(x),
        #    'textile': lambda x: textile(x),
        #    }[self.markup_type](self.markup)

        self.markup_html = getattr(MarkupParser(), self.markup_type,
            'default')(self.markup)
        return super(MarkupContent, self).save(*args, **kwargs)

    def render(self, request, **kwargs):
        context = RequestContext(request, {'content': self,})
        return render_to_string(self.template, context)
