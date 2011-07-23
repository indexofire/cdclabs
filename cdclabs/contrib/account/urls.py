# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

"""
Urls overview in form "url name: short description":

 * auth_login: log in form
 * auth_logout: log out view
 * auth_logout_successfull: the page after successful log out
 * registration_register: sign up form
 * registration_complete: the page after successful registration
 * activation_required: the page with activation remainder
        which shows after filling the registration form
 * auth_password_reset: form for password reset by anonymous user
 * auth_password_change: form for password change by loged in user
 * auth_password_change_done: page after success password change
 * auth_email_change: form for email change
 * auth_email_change_done: the page after success email change
"""

urlpatterns = patterns('contrib.account.views',
    url(r'^login/$', 'login', name='auth_login'),
    url(r'^logout/$', 'logout', name='auth_logout'),
    url(r'^logout/successful/$', 'logout_successful', name='auth_logout_successful'),

    # Registration
    #url(r'^registration/$', 'registration', name='registration_register'),
    #url(r'^activation/required/$', direct_to_template, {'template':'account/activation_required.html'}, name='activation_required'),
    #url(r'^registration/complete/$', direct_to_template, {'template':'account/registration_complete.html'}, name='registration_complete'),

    # Password management
    url(r'^password/reset/$', 'password_reset',
        name='auth_password_reset'),
    url(r'^password/change/$', 'password_change',
        name='auth_password_change'),
    url(r'^password/change/done/$', 'password_change_done',
        name='auth_password_change_done'),

    # Email management
    url(r'^email/change/$', 'email_change', name='auth_email_change'),
    url(r'^email/change/done/$', 'email_change_done',
        name='auth_email_change_done'),
)
