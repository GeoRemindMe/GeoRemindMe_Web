# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'UserProfile.accepted_eula'
        db.delete_column('geouser_userprofile', 'accepted_eula')

        # Deleting field 'UserProfile.favorite_animal'
        db.delete_column('geouser_userprofile', 'favorite_animal')

        # Adding field 'UserProfile.avatar'
        db.add_column('geouser_userprofile', 'avatar', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'UserProfile.sync_avatar_with'
        db.add_column('geouser_userprofile', 'sync_avatar_with', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1), keep_default=False)

        # Changing field 'UserProfile.notification_account'
        db.alter_column('geouser_userprofile', 'notification_account', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'UserProfile.notification_invitation'
        db.alter_column('geouser_userprofile', 'notification_invitation', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'UserProfile.notification_suggestion'
        db.alter_column('geouser_userprofile', 'notification_suggestion', self.gf('django.db.models.fields.PositiveSmallIntegerField')())


    def backwards(self, orm):
        
        # Adding field 'UserProfile.accepted_eula'
        db.add_column('geouser_userprofile', 'accepted_eula', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'UserProfile.favorite_animal'
        db.add_column('geouser_userprofile', 'favorite_animal', self.gf('django.db.models.fields.CharField')(default='Dragons.', max_length=20), keep_default=False)

        # Deleting field 'UserProfile.avatar'
        db.delete_column('geouser_userprofile', 'avatar')

        # Deleting field 'UserProfile.sync_avatar_with'
        db.delete_column('geouser_userprofile', 'sync_avatar_with')

        # Changing field 'UserProfile.notification_account'
        db.alter_column('geouser_userprofile', 'notification_account', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UserProfile.notification_invitation'
        db.alter_column('geouser_userprofile', 'notification_invitation', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'UserProfile.notification_suggestion'
        db.alter_column('geouser_userprofile', 'notification_suggestion', self.gf('django.db.models.fields.IntegerField')())


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geouser.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_account': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'notification_invitation': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'notification_suggestion': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'show_followers': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sync_avatar_with': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['geouser']
