# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'discussion_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'discussion', ['Category'])

        # Adding model 'Post'
        db.create_table(u'discussion_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['discussion.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('reply_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'child', null=True, to=orm['discussion.Post'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
        ))
        db.send_create_signal(u'discussion', ['Post'])

        # Adding model 'Announcement'
        db.create_table(u'discussion_announcement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'announcers', to=orm['account.User'])),
            ('announce_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('announce_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'discussion', ['Announcement'])

        # Adding M2M table for field mark_as_read on 'Announcement'
        m2m_table_name = db.shorten_name(u'discussion_announcement_mark_as_read')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('announcement', models.ForeignKey(orm[u'discussion.announcement'], null=False)),
            ('user', models.ForeignKey(orm[u'account.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['announcement_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'discussion_category')

        # Deleting model 'Post'
        db.delete_table(u'discussion_post')

        # Deleting model 'Announcement'
        db.delete_table(u'discussion_announcement')

        # Removing M2M table for field mark_as_read on 'Announcement'
        db.delete_table(db.shorten_name(u'discussion_announcement_mark_as_read'))


    complete_apps = ['discussion']