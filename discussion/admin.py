# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.contrib import admin
import reversion

from models import Category, Post, Announcement


# initiate logger
logging.getLogger(__name__)


class AnnouncementAdmin(reversion.VersionAdmin):
    """ AnnouncementAdmin
    """
    list_display = ['title', 'created_at', 'created_by']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super(AnnouncementAdmin, self).save_model(request, obj, form, change)


class CategoryAdmin(reversion.VersionAdmin):
    """ CategoryAdmin
    """
    list_display = ['name', 'is_active']


class PostAdmin(admin.ModelAdmin):
    """ PostAdmin
    """
    list_display = ['title', 'category', 'created_by', 'reply_to', 'created_at']
    readonly_fields = ['title', 'category', 'created_by', 'reply_to', 'created_at', 'body']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Category, CategoryAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Post, PostAdmin)
