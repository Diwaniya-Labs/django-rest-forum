# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from views import PostViewSet, CategoryViewSet, AnnouncementViewSet


category_list = CategoryViewSet.as_view({
    'get': 'list',
})

category_detail = CategoryViewSet.as_view({
    'get': 'retrieve',
})

announcement_list = AnnouncementViewSet.as_view({
    'get': 'list',
})

announcement_detail = AnnouncementViewSet.as_view({
    'get': 'retrieve',
})

post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns(patterns('',

                                              url(r'^category/$', category_list, name='category-list'),
                                              url(r'^category/(?P<pk>[0-9]+)/$', category_detail,
                                                  name='category-detail'),

                                              url(r'^announcement/$', announcement_list, name='announcement-list'),
                                              url(r'^announcement/(?P<pk>[0-9]+)/$', announcement_detail,
                                                  name='announcement-detail'),

                                              url(r'^post/$', post_list, name='post-list'),
                                              url(r'^post/(?P<pk>[0-9]+)/$', post_detail,
                                                  name='post-detail'),

))