# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from rest_framework import viewsets

from permissions import CategoryPermissions, PostPermissions, AnnouncementPermissions
from models import Category, Post, Announcement
from serializers import CategorySerializer, PostSerializer, AnnouncementSerializer


# initiate logger
logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    """ CategoryViewSet
        Returns all active categories which can be used for placing a new discussion under
    * this web service only accessible for query
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (CategoryPermissions, )

    def get_queryset(self):
        """ Only active categories
        """
        return Category.objects.filter(is_active=True)


class PostViewSet(viewsets.ModelViewSet):
    """PostViewSet
        Post API will be used to creating new discussion, listing, and replying to a post

    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermissions, )

    def pre_save(self, obj):
        obj.created_by = self.request.user

    def get_queryset(self):
        """
        """
        return Post.objects.filter(reply_to__isnull=True)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """AnnouncementViewSet
    announcements can only be retrieved by authorized users

    * if announcement has been retrieved by user X, user X will no more see the announcement
    as it will be marked as read
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (AnnouncementPermissions, )

    def retrieve(self, request, *args, **kwargs):
        response = super(AnnouncementViewSet, self).retrieve(request, *args, **kwargs)
        if self.object.mark_as_read.filter(id=request.user.id).count() is 0:
            self.object.mark_as_read.add(request.user)
        return response