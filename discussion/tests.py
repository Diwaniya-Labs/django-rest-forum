# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from django.core import management

from account.models import User
from models import Announcement


class AnnouncementTestCase(TestCase):
    """AnnouncementTestCase"""

    def setUp(self):
        """ AnnouncementTestCase setup / creating user's pragmatically via objects api """
        self.c = APIClient()
        User.objects.create_user(username="lion", email="roar@gmail.com", password="password")
        User.objects.create_guest(username="cat")
        self.register_users_via_api()
        Announcement.objects.create(title=u'This is the first test announcement', body=u'the first announcement body',
                                    created_by_id=1)
        Announcement.objects.create(title=u'This is the second test announcement', body=u'the second announcement body',
                                    created_by_id=1)

    def register_users_via_api(self):
        """ Registering users using rest framework API """
        response = self.c.post(reverse('user-create-guest'), {'username': 'rest_lion'})
        self.assertEqual(response.status_code, 201, "Cannot create user 'guest' (rest_lion)")
        response = self.c.post(reverse('user-list'),
                               {'username': 'rest_cat', 'password': 'password', 'email': 'xx@gmail.com'})
        self.assertEqual(response.status_code, 201, "Cannot create user 'registered' (rest_cat)")

    def test_list_announcements_as_registered(self):
        """ Test listing all new announcements as registered user """
        # authenticate
        response = self.c.post("/api/account/api-token-auth/", {'username': 'lion', 'password': 'password'})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('announcement-list'), {}, **header)
        self.assertEqual(response.data.get('count'), 2, 'Did not return all the new announcements')
        self.assertEqual(response.status_code, 200, 'Failed to retrieve all announcements')

    def test_list_announcements_as_guest(self):
        """ Test listing all new announcements as guest user """
        # authenticate
        # use the guest username as md5 password with key
        p = hashlib.md5()
        p.update('cat%s' % getattr(settings, 'GUEST_PASSWORD_APPEND_KEY'))
        response = self.c.post("/api/account/api-token-auth/", {'username': 'cat', 'password': p.hexdigest()})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('announcement-list'), {}, **header)
        self.assertEqual(response.data.get('count'), 2, 'Did not return all the new announcements')
        self.assertEqual(response.status_code, 200, 'Failed to retrieve all announcements')

    def test_marking_announcement_as_read_by_registered_user(self):
        """ Test marking an announcement as read by registered user"""
        # authenticate
        response = self.c.post("/api/account/api-token-auth/", {'username': 'lion', 'password': 'password'})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('announcement-list'), {}, **header)
        self.assertEqual(response.data.get('count'), 2, 'Did not return all the new announcements')

    def test_marking_announcement_as_read_by_guest_user(self):
        """ Test marking an announcement as read by guest user"""
        # authenticate
        # use the guest username as md5 password with key
        p = hashlib.md5()
        p.update('cat%s' % getattr(settings, 'GUEST_PASSWORD_APPEND_KEY'))
        response = self.c.post("/api/account/api-token-auth/", {'username': 'cat', 'password': p.hexdigest()})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('announcement-list'), {}, **header)
        self.assertEqual(response.data.get('count'), 2, 'Did not return all the new announcements')


class PostTestCase(TestCase):
    """PostTestCase"""

    def setUp(self):
        """ PostTestCase setup / creating user's pragmatically via objects api """
        self.c = APIClient()
        User.objects.create_user(username="lion", email="roar@gmail.com", password="password")
        User.objects.create_guest(username="cat")
        self.register_users_via_api()

    def register_users_via_api(self):
        """ Registering users using rest framework API """
        response = self.c.post(reverse('user-create-guest'), {'username': 'rest_lion'})
        self.assertEqual(response.status_code, 201, "Cannot create user 'guest' (rest_lion)")
        response = self.c.post(reverse('user-list'),
                               {'username': 'rest_cat', 'password': 'password', 'email': 'xx@gmail.com'})
        self.assertEqual(response.status_code, 201, "Cannot create user 'registered' (rest_cat)")

    def test_create_post_as_registered(self):
        """ Test creating a new post as registered user"""
        # authenticate
        response = self.c.post("/api/account/api-token-auth/", {'username': 'lion', 'password': 'password'})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('category-list'), {}, **header)

        response = self.c.post(reverse('post-list'), {'title': 'my post about dl',
                                                      'body': 'am enjoying the game folks',
                                                      'category': response.data.get('results')[0].get('url')}, **header)
        self.assertEqual(response.status_code, 201, 'Failed to create a new post')

    def test_create_post_as_guest(self):
        """ Test creating a new post as guest user"""
        # authenticate
        # use the guest username as md5 password with key
        p = hashlib.md5()
        p.update('cat%s' % getattr(settings, 'GUEST_PASSWORD_APPEND_KEY'))
        response = self.c.post("/api/account/api-token-auth/", {'username': 'cat', 'password': p.hexdigest()})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('category-list'), {}, **header)

        response = self.c.post(reverse('post-list'), {'title': 'my post about dl',
                                                      'body': 'am enjoying the game folks',
                                                      'category': response.data.get('results')[0].get('url')}, **header)
        self.assertEqual(response.status_code, 403, 'Creating a post should fail when posting as guest')

    def test_replying_to_a_post(self):
        """ Replying to a post """
        # authenticate
        response = self.c.post("/api/account/api-token-auth/", {'username': 'lion', 'password': 'password'})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('category-list'), {}, **header)
        category_url = response.data.get('results')[0].get('url')
        response = self.c.post(reverse('post-list'), {'title': 'my post about dl',
                                                      'body': 'am enjoying the game folks',
                                                      'category': category_url}, **header)
        self.assertEqual(response.status_code, 201, 'Creating a post should fail when posting as guest')
        response = self.c.post(reverse('post-list'), {'title': 'my reply to a post',
                                                      'reply_to': response.data.get('url'),
                                                      'body': 'am enjoying the game folks',
                                                      'category': category_url}, **header)
        self.assertEqual(response.status_code, 201, 'Creating a post should fail when posting as guest')

    def test_retrieve_post_with_replies(self):
        """ Test retrieving a post with all replies """
        # authenticate
        response = self.c.post("/api/account/api-token-auth/", {'username': 'lion', 'password': 'password'})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('category-list'), {}, **header)
        category_url = response.data.get('results')[0].get('url')
        response = self.c.post(reverse('post-list'), {'title': 'my post about dl',
                                                      'body': 'am enjoying the game folks',
                                                      'category': category_url}, **header)
        self.assertEqual(response.status_code, 201, 'Creating a post should fail when posting as guest')
        post_url = response.data.get('url')
        response = self.c.post(reverse('post-list'), {'title': 'my reply to a post',
                                                      'reply_to': post_url,
                                                      'body': 'am enjoying the game folks',
                                                      'category': category_url}, **header)
        self.assertEqual(response.status_code, 201, 'Creating a post should fail when posting as guest')

        response = self.c.post(reverse('post-list'), {'title': 'my reply to a post 2',
                                                      'reply_to': post_url,
                                                      'body': 'am enjoying the game folks 2',
                                                      'category': category_url}, **header)
        self.assertEqual(response.status_code, 201, 'Creating a post should fail when posting as guest')

        response = self.c.get(reverse('post-list'), {}, **header)
        response = self.c.get(response.data.get('results')[0].get('url'), {}, **header)
        self.assertEqual(len(response.data.get('replies')), 2, 'Two replies were not found in the response chain')

    def test_replying_to_a_reply(self):
        """ Test replying to a reply """
        # authenticate
        response = self.c.post("/api/account/api-token-auth/", {'username': 'lion', 'password': 'password'})
        self.assertEqual(response.status_code, 200, "User couldn't log in")
        token = response.data['token']
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(token)}

        response = self.c.get(reverse('category-list'), {}, **header)
        category_url = response.data.get('results')[0].get('url')
        response = self.c.post(reverse('post-list'), {'title': 'my post about dl',
                                                      'body': 'am enjoying the game folks',
                                                      'category': category_url}, **header)
        self.assertEqual(response.status_code, 201, 'Creating a post should fail when posting as guest')

        response = self.c.post(reverse('post-list'), {'title': 'my reply to a post',
                                                      'reply_to': response.data.get('url'),
                                                      'body': 'am enjoying the game folks',
                                                      'category': category_url}, **header)
        self.assertEqual(response.status_code, 201, 'Creating a post should fail when posting as guest')

        response = self.c.post(reverse('post-list'), {'title': 'my reply to a post 2',
                                                      'reply_to': response.data.get('url'),
                                                      'body': 'am enjoying the game folks 2',
                                                      'category': category_url}, **header)
        self.assertEqual(response.data.get('non_field_errors')[0], u'You cannot reply to a reply',
                         'Error a reply to a reply passed without validation')
