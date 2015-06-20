# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Submit'
        db.create_table('collector_submit', (
            ('sid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('source', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(default='', max_length=3)),
            ('source_file', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('exec_file', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('log', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('check_battle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collector.Battle'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PD', max_length=2)),
        ))
        db.send_create_signal('collector', ['Submit'])

        # Adding model 'Battle'
        db.create_table('collector_battle', (
            ('player1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='played1', to=orm['collector.Submit'])),
            ('player2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='played2', to=orm['collector.Submit'])),
            ('score', self.gf('django.db.models.fields.CharField')(default='?-?', max_length=200)),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='wins', null=True, to=orm['collector.Submit'])),
            ('serial', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['collector.BattleSerial'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PD', max_length=2)),
        ))
        db.send_create_signal('collector', ['Battle'])

        # Adding model 'BattleSerial'
        db.create_table('collector_battleserial', (
            ('sid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='serplayed1', to=orm['collector.Submit'])),
            ('player2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='serplayed2', to=orm['collector.Submit'])),
            ('games', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('played', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score2', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['collector.Submit'], null=True, blank=True)),
            ('failed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('started', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('collector', ['BattleSerial'])


    def backwards(self, orm):
        # Deleting model 'Submit'
        db.delete_table('collector_submit')

        # Deleting model 'Battle'
        db.delete_table('collector_battle')

        # Deleting model 'BattleSerial'
        db.delete_table('collector_battleserial')


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
        'collector.battle': {
            'Meta': {'object_name': 'Battle'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'player1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'played1'", 'to': "orm['collector.Submit']"}),
            'player2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'played2'", 'to': "orm['collector.Submit']"}),
            'score': ('django.db.models.fields.CharField', [], {'default': "'?-?'", 'max_length': '200'}),
            'serial': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['collector.BattleSerial']", 'null': 'True', 'blank': 'True'}),
            'sid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PD'", 'max_length': '2'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'wins'", 'null': 'True', 'to': "orm['collector.Submit']"})
        },
        'collector.battleserial': {
            'Meta': {'object_name': 'BattleSerial'},
            'failed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'games': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'played': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'player1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'serplayed1'", 'to': "orm['collector.Submit']"}),
            'player2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'serplayed2'", 'to': "orm['collector.Submit']"}),
            'score1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'started': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Submit']", 'null': 'True', 'blank': 'True'})
        },
        'collector.submit': {
            'Meta': {'object_name': 'Submit'},
            'check_battle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collector.Battle']", 'null': 'True', 'blank': 'True'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exec_file': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '3'}),
            'log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {}),
            'source_file': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PD'", 'max_length': '2'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['collector']