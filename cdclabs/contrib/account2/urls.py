# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from .views import *


urlpatterns = patterns('',
    url(r'^signup/$', view=SignupLoginView.as_view(
        featured_form_mixin_class=SignupMultipleFormMixin),
        name='account_signup'),
    url(r'^login/$', view=SignupLoginView.as_view(
        featured_form_mixin_class=LoginMultipleFormMixin),
        name='account_login'),
    url(r'^logout/$', view=LogoutView.as_view(), name='account_logout'),
    url(r'^signup-login/$', view=SignupLoginView.as_view(),
        name='account_signup_login'),
    url(r'^iframes/signup/$', view=SignupLoginIframeView.as_view(
        featured_form_mixin_class=SignupIframeMultipleFormMixin),
        name='account_signup_iframe'),
    url(r'^iframes/login/$', view=SignupLoginIframeView.as_view(
        featured_form_mixin_class=LoginIframeMultipleFormMixin),
        name='account_login_iframe'),
    url(r'^iframes/signup-login/$', view=SignupLoginIframeView.as_view(),
        name='account_signup_login_iframe'),
    url(r'^iframes/signup-login/success/$',
        view=SignupLoginSuccessIframeView.as_view(),
        name='account_signup_login_success_iframe'),
)
