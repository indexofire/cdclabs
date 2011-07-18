# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseForbidden
from feincms.module.page.models import Page
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent
from contrib.content.googlemaps.models import GoogleMapsContent
from contrib.content.markup.models import MarkupContent
from contrib.form_designer.models import FormContent


# Register page extensions
Page.register_extensions(
    'datepublisher',
    'translations',
    'changedate',
    'navigation',
    'seo',
    'symlinks',
    'titles',
    'contrib.extension.page.auth',
)

# Register Templates used in pages
Page.register_templates(
    {
        'key': 'base',
        'title': _('Standard Template'),
        'path': 'base.html',
        'regions': (
            ('main', _('Main content area')),
            ('sidebar', _('Sidebar'), 'inherited'),
        ),
    },
    {
        'key': 'two',
        'title': _('Two Columns Page'),
        'path': 'col_two.html',
        'regions': (
            ('main', _('Main content area')),
            ('right', _('Right'), 'inherited'),
        ),
    },
    {
        'key': 'three',
        'title': _('Three Columns Page'),
        'path': 'col_three.html',
        'regions': (
            ('main', _('Main content area')),
            ('sidebar', _('Sidebar'), 'inherited'),
            ('right', _('Right')),
        ),
    },
    {
        'key': 'main',
        'title': _('Main Page'),
        'path': 'main.html',
        'regions': (
            ('main', _('Main content area')),
        ),
    },
)


# Add rich content type
Page.create_content_type(RichTextContent)

# Add image content type
Page.create_content_type(
    ImageContent,
    POSITION_CHOICES=(
        ('block', _('block')),
        ('left', _('left')),
        ('right', _('right')),
    )
)
# Add markup content type
Page.create_content_type(MarkupContent)

# Add google maps content type
Page.create_content_type(GoogleMapsContent)

# Add forum application
Page.create_content_type(
    ApplicationContent,
    APPLICATIONS=(
        ('forum.urls', 'Forum Application'),
    )
)

# Add form content type
Page.create_content_type(FormContent)
