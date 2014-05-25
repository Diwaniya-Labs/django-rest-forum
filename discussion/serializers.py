# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from rest_framework import serializers

from models import Category, Post, Announcement


# initiate logger
logging.getLogger(__name__)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    CategorySerializer
    """

    class Meta:
        model = Category


class PostRepliesSerializer(serializers.HyperlinkedModelSerializer):
    """
    PostRepliesSerializer
    will return replies of a specific post
    """

    class Meta:
        model = Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    PostSerializer
    """
    created_by = serializers.IntegerField(source='created_by', read_only=True)
    replies = serializers.SerializerMethodField('get_replies')

    class Meta:
        model = Post

    def get_replies(self, obj):
        serializer = PostRepliesSerializer(Post.objects.filter(reply_to=obj), many=True,
                                           context={'request': self.context.get('request')})
        return serializer.data

    def validate(self, attrs):
        """
        """
        if attrs['reply_to']:
            if attrs['reply_to'].reply_to:
                raise serializers.ValidationError('You cannot reply to a reply')
        return attrs


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    """
    AnnouncementSerializer
    """
    marked_as_read = serializers.SerializerMethodField('get_marked_as_read_flag')

    class Meta:
        model = Announcement
        exclude = ('mark_as_read', 'created_by')

    def get_marked_as_read_flag(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous():
            return False
        if obj.mark_as_read.filter(pk=user.pk).count():
            return True
        return False