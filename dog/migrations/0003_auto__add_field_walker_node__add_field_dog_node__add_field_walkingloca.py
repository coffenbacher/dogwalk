# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Walker.node'
        db.add_column(u'dog_walker', 'node',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['route.Node']),
                      keep_default=False)

        # Adding field 'Dog.node'
        db.add_column(u'dog_dog', 'node',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['route.Node']),
                      keep_default=False)

        # Adding field 'WalkingLocation.node'
        db.add_column(u'dog_walkinglocation', 'node',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['route.Node']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Walker.node'
        db.delete_column(u'dog_walker', 'node_id')

        # Deleting field 'Dog.node'
        db.delete_column(u'dog_dog', 'node_id')

        # Deleting field 'WalkingLocation.node'
        db.delete_column(u'dog_walkinglocation', 'node_id')


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
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['route.Node']"})
        },
        u'dog.requiredwalk': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'RequiredWalk'},
            'after': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'before': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'days': ('django.db.models.fields.BigIntegerField', [], {'default': 'None'}),
            'dog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Dog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'dog.walker': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Walker'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['route.Node']"})
        },
        u'dog.walkinglocation': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'WalkingLocation'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['route.Node']"})
        },
        u'route.node': {
            'Meta': {'object_name': 'Node'},
            'address': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['dog']