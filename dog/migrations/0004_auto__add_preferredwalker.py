# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PreferredWalker'
        db.create_table(u'dog_preferredwalker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('dog', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dog.Dog'], unique=True)),
            ('walker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dog.Walker'])),
        ))
        db.send_create_signal(u'dog', ['PreferredWalker'])


    def backwards(self, orm):
        # Deleting model 'PreferredWalker'
        db.delete_table(u'dog_preferredwalker')


    models = {
        u'dog.cancelledwalk': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'CancelledWalk'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'dog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cancellations'", 'to': u"orm['dog.Dog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
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
        u'dog.preferredwalker': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'PreferredWalker'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dog': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dog.Dog']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'walker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Walker']"})
        },
        u'dog.requiredwalk': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'RequiredWalk'},
            'after': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'before': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.BigIntegerField', [], {'default': 'None'}),
            'dog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requiredwalks'", 'to': u"orm['dog.Dog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'until': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dog.walker': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Walker'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': "'13:00:00'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'walkers'", 'to': u"orm['graph.Node']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': "'08:00:00'"})
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
            'seconds': ('django.db.models.fields.FloatField', [], {'default': '120'})
        }
    }

    complete_apps = ['dog']