# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from rest_framework import permissions


# initiate logger
logging.getLogger(__name__)


class CategoryPermissions(permissions.DjangoModelPermissions):
    """CategoryPermissions"""


class PostPermissions(permissions.DjangoModelPermissions):
    """PostPermissions"""


class AnnouncementPermissions(permissions.DjangoModelPermissions):
    """AnnouncementPermissions"""

