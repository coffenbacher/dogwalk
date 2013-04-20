# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dog'
        db.create_table(u'dog_dog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('days', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('node', self.gf('django.db.models.fields.related.OneToOneField')(related_name='dog', unique=True, blank=True, to=orm['graph.Node'])),
        ))
        db.send_create_signal(u'dog', ['Dog'])

        # Adding M2M table for field incompatible on 'Dog'
        db.create_table(u'dog_dog_incompatible', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_dog', models.ForeignKey(orm[u'dog.dog'], null=False)),
            ('to_dog', models.ForeignKey(orm[u'dog.dog'], null=False))
        ))
        db.create_unique(u'dog_dog_incompatible', ['from_dog_id', 'to_dog_id'])

        # Adding model 'RequiredWalk'
        db.create_table(u'dog_requiredwalk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('dog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requiredwalks', to=orm['dog.Dog'])),
            ('after', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('before', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('days', self.gf('django.db.models.fields.BigIntegerField')(default=None)),
        ))
        db.send_create_signal(u'dog', ['RequiredWalk'])

        # Adding model 'Walker'
        db.create_table(u'dog_walker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='walkers', to=orm['graph.Node'])),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')(default=9)),
        ))
        db.send_create_signal(u'dog', ['Walker'])

        # Adding model 'WalkingLocation'
        db.create_table(u'dog_walkinglocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
        ))
        db.send_create_signal(u'dog', ['WalkingLocation'])


    def backwards(self, orm):
        # Deleting model 'Dog'
        db.delete_table(u'dog_dog')

        # Removing M2M table for field incompatible on 'Dog'
        db.delete_table('dog_dog_incompatible')

        # Deleting model 'RequiredWalk'
        db.delete_table(u'dog_requiredwalk')

        # Deleting model 'Walker'
        db.delete_table(u'dog_walker')

        # Deleting model 'WalkingLocation'
        db.delete_table(u'dog_walkinglocation')


    models = {
        u'dog.dog': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Dog'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incompatible': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dog.Dog']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'node': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'dog'", 'unique': 'True', 'blank': 'True', 'to': u"orm['graph.Node']"})
        },
        u'dog.requiredwalk': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'RequiredWalk'},
            'after': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'before': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days': ('django.db.models.fields.BigIntegerField', [], {'default': 'None'}),
            'dog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requiredwalks'", 'to': u"orm['dog.Dog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'dog.walker': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Walker'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'walkers'", 'to': u"orm['graph.Node']"})
        },
        u'dog.walkinglocation': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'WalkingLocation'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"})
        },
        u'graph.node': {
            'Meta': {'object_name': 'Node'},
            'address': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seconds': ('django.db.models.fields.FloatField', [], {'default': '420'})
        }
    }

    complete_apps = ['dog']