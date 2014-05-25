# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.conf import settings
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.translation import ugettext_lazy as _


# initiate logger
logging.getLogger(__name__)


class Category(models.Model):
    """ Category
    """
    name = models.CharField(_('Name'), max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = _('Categories')

    def __str__(self):
        # Use django.utils.encoding.force_bytes() because value returned is unicode
        return force_bytes('%s' % self.name)

    def __unicode__(self):
        return u'%s' % self.name


class Post(models.Model):
    """ Post
    """
    category = models.ForeignKey(Category)
    title = models.CharField(_('Title'), max_length=200)
    body = models.TextField(_('Body'), )
    reply_to = models.ForeignKey('self', blank=True, null=True, related_name='child')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL'))

    def __str__(self):
        # Use django.utils.encoding.force_bytes() because value returned is unicode
        return force_bytes('%s' % self.title)

    def __unicode__(self):
        return u'%s' % self.title


class Announcement(models.Model):
    """ Announcement
    """
    title = models.CharField(_('Title'), max_length=200)
    body = models.TextField(_('Body'), )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL'), related_name='announcers', editable=False)
    announce_from = models.DateTimeField(_('Announce from'), null=True, blank=True)
    announce_to = models.DateTimeField(_('Announce to'), null=True, blank=True)
    mark_as_read = models.ManyToManyField(getattr(settings, 'AUTH_USER_MODEL'), related_name='announcements',
                                          editable=False)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        # Use django.utils.encoding.force_bytes() because value returned is unicode
        return force_bytes('%s' % self.title)

    def __unicode__(self):
        return u'%s' % self.title
