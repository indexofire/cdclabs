# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import (
    patterns,
    include,
    url,
)
from django.contrib import admin
from django.views.generic.simple import redirect_to
from feincms.module.page.sitemap import PageSitemap


admin.autodiscover()
sitemaps = {'pages' : PageSitemap}

urlpatterns = patterns('',
    url(r'^favicon\.ico/$', redirect_to, {'url': '/media/favicon.ico'}),
    url(r'^mercury/', include('mercury.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('contrib.account.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^profile/', include('contrib.profile.urls')),
    #url(r'^$', 'feincms.views.base.handler', name='feincms_home'),
    #url(r'^(.*)/$', 'feincms.views.base.handler', name='feincms_handler'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT},
        ),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT},
        ),
    )

urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps},
    ),
)

urlpatterns += patterns('',
    url(r'', include('feincms.urls')),
)
