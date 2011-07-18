# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

__key__ = ''

class GoogleMapsContent(models.Model):
    """
    Google Maps API v3
    """
    # map type choices:
    #MAP_TYPE_CHOICES = (
    #    (),
    #    (),
    #    ()
    #)
    #map_type = models.CharField(
    #    _("Map Type"),
    #    blank=False,
    #    null=False,
    #    default='ROADMAP',
    #)
    title = models.CharField(
        _("Title"),
        max_length=100,
        blank=True,
        null=True,
    )
    # leave the real address
    address = models.CharField(
        _("Address"),
        max_length=150,
        blank=True,
        null=True,
    )
    zipcode = models.CharField(
        _("Zip Code"),
        max_length=30,
        blank=True,
        null=True,
    )
    content = models.CharField(
        _("Additional Content"),
        max_length=255,
        blank=True,
        null=True,
    )
    city = models.CharField(
        _("City Name"),
        max_length=100,
        blank=True,
        null=True,
    )
    zoom = models.IntegerField(
        _("zoom level"),
        blank=True,
        null=True,
        default=13,
    )
    lat = models.DecimalField(
        _('latitude'),
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_('use latitude to define the map possiton'),
    )
    lng = models.DecimalField(
        _('longitude'),
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
        help_text=_('use longitude to define the map possiton'),
    )
    #route_planer_title = models.CharField(_("route planer title"), max_length=150, blank=True, null=True, help_text=_("calculate your fastest way to here"))
    #route_planer = models.BooleanField(_("route planer"), default=False)

    class Meta:
        abstract = True

    def get_lat_lng(self):
        if self.lat and self.lng:
            return [self.lat, self.lng]

    @property
    def media(self):
        return forms.Media(
            css={},
            js=('googlemaps/js/googlemaps.js'),
        )

    def render(self, **kwargs):
        return render_to_string('googlemaps/default.html', {'object': self})
