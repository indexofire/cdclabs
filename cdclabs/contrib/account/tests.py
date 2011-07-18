# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import pickle
import cgi
from django.test import TestCase
from django.test.client import Client
from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from urlauth.util import wrap_url
from account.util import str_to_class
from account import settings as app_settings

UserModel = str_to_class(app_settings.USER_MODEL)

class AccountTestCase(TestCase):
    urls = 'account.tests'

    def setUp(self):
        UserModel.objects.all().delete()
        u = UserModel(username='user', email='user@host.com')
        u.set_password('pass')
        u.is_active = True
        u.save()
        self.user = u

        u = UserModel(username='ban_user', email='ban_user@host.com')
        u.set_password('pass')
        u.is_active = False
        u.save()
        self.ban_user = u


class SignalsTestCase(AccountTestCase):

    def testActivation(self):
        def process_url(url, **kwargs):
           url = wrap_url(url, **kwargs)
           return url.split('?')[0], cgi.parse_qs(url.split('?')[1])

        test_url = '/account_test_view/'
        expired = datetime.now() + timedelta(days=1)
        resp = self.client.get(test_url)


        # Activation of baned user
        self.client.logout()
        url, args = process_url(test_url, uid=self.ban_user.id, expired=expired, action='activation')
        resp = self.client.get(url, args)
        self.assertEqual(self.client.session['_auth_user_id'], self.ban_user.id)
        self.client.session.flush()

        # New password
        #self.client.logout()
        #url, args = process_url(test_url, uid=self.user.id, expired=expired,
                                #action='new_password', password='foobar')
        #self.assertTrue(authenticate(uid=self.user.id, password='pass'))
        #resp = self.client.get(url, args)
        #self.assertEqual(self.client.session['_auth_user_id'], self.user.id)
        #self.client.session.flush()
        #self.assertTrue(authenticate(uid=self.user.id, password='foobar'))
        #self.client.session.flush()

        # New email
        self.client.logout()
        expired = datetime.now() + timedelta(days=1)
        url, args = process_url(test_url, uid=self.user.id, expired=expired,
                                action='new_email', email='user_gaz@host.com')
        self.assertEqual('user@host.com', self.user.email)
        resp = self.client.get(url, args)
        self.assertEqual(self.client.session['_auth_user_id'], self.user.id)
        user = UserModel.objects.get(pk=self.user.id)
        self.assertEqual(user.email, 'user_gaz@host.com')


def test_view(request):
    return HttpResponse()

urlpatterns = patterns('',
    url('account_test_view/', test_view, name='account_test_view'),
)
