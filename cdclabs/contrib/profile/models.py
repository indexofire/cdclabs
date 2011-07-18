# -*- coding: utf-8 -*-
import re, datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField


class Profile(models.Model):
    """Profile model"""
    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
        (3, _('Other')),
    )
    user = models.ForeignKey(User, unique=True)
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    mugshot = models.FileField(_('mugshot'), upload_to='mugshots', blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    address1 = models.CharField(_('address1'), blank=True, max_length=100)
    address2 = models.CharField(_('address2'), blank=True, max_length=100)
    city = models.CharField(_('city'), blank=True, max_length=100)
    state = models.CharField(_('state'), blank=True, max_length=100, help_text='or Province')
    zip = models.CharField(_('zip'), blank=True, max_length=10)
    country = models.CharField(_('country'), blank=True, max_length=100)
    mobile = PhoneNumberField(_('mobile'), blank=True)
    #company = models.CharField(_('company'), blank=True, max_length=255)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        db_table = 'user_profiles'

    def __unicode__(self):
        return u"%s" % self.user.get_full_name()

    @property
    def age(self):
		today = datetime.date.today()
		try:
			birth = self.birth_date.replace(year=today.year)
		except ValueError:
			birth = self.birth_date.replace(year=today.year, day=self.birth_date.day-1)
		if birth > today:
			return today.year - self.birth_date.year - 1
		else:
			return today.year - self.birth_date.year

    @permalink
    def get_absolute_url(self):
        return ('profile_detail', None, { 'username': self.user.username })

    @property
    def sms_address(self):
        if (self.mobile and self.mobile_provider):
            return u"%s@%s" % (re.sub('-', '', self.mobile), self.mobile_provider.domain)


class ServiceType(models.Model):
    """Service type model"""
    title = models.CharField(_('title'), blank=True, max_length=100)
    url = models.URLField(_('url'), blank=True, help_text='URL with a single \'{user}\' placeholder to turn a username into a service URL.', verify_exists=False)

    class Meta:
        verbose_name = _('service type')
        verbose_name_plural = _('service types')
        db_table = 'user_service_types'

    def __unicode__(self):
        return u"%s" % self.title


class Service(models.Model):
    """Service model"""
    service = models.ForeignKey(ServiceType)
    profile = models.ForeignKey(Profile)
    username = models.CharField(_('Name or ID'), max_length=100, help_text="Username or id to be inserted into the service url.")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        db_table = 'user_services'

    def __unicode__(self):
        return u"%s" % self.username

    @property
    def service_url(self):
        return re.sub('{user}', self.username, self.service.url)

    @property
    def title(self):
        return u"%s" % self.service.title


class Link(models.Model):
    """Service type model"""
    profile = models.ForeignKey(Profile)
    title = models.CharField(_('title'), max_length=100)
    url = models.URLField(_('url'), verify_exists=True)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        db_table = 'user_links'

    def __unicode__(self):
        return u"%s" % self.title
