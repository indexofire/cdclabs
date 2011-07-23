# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import (
    patterns,
    include,
    url,
)
from django.contrib import admin
from django.views.generic.simple import redirect_to


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^favicon\.ico/$', redirect_to, {'url': '/media/favicon.ico'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('contrib.account.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^profile/', include('contrib.profile.urls')),
)

urlpatterns += patterns('',
    url(r'', include('feincms.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
	    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
	        {'document_root': settings.MEDIA_ROOT},
	    ),
    )
