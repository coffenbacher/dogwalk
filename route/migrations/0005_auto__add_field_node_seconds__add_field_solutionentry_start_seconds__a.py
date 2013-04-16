# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Node.seconds'
        db.add_column(u'route_node', 'seconds',
                      self.gf('django.db.models.fields.FloatField')(default=420),
                      keep_default=False)

        # Adding field 'SolutionEntry.start_seconds'
        db.add_column(u'route_solutionentry', 'start_seconds',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'SolutionEntry.end_seconds'
        db.add_column(u'route_solutionentry', 'end_seconds',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Node.seconds'
        db.delete_column(u'route_node', 'seconds')

        # Deleting field 'SolutionEntry.start_seconds'
        db.delete_column(u'route_solutionentry', 'start_seconds')

        # Deleting field 'SolutionEntry.end_seconds'
        db.delete_column(u'route_solutionentry', 'end_seconds')


    models = {
        u'route.edge': {
            'Meta': {'object_name': 'Edge'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meters': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['route.Node']", 'symmetrical': 'False'}),
            'seconds': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'route.node': {
            'Meta': {'object_name': 'Node'},
            'address': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seconds': ('django.db.models.fields.FloatField', [], {'default': '420'})
        },
        u'route.problem': {
            'Meta': {'object_name': 'Problem'},
            'end': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ending_at'", 'symmetrical': 'False', 'to': u"orm['route.Node']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'starting_at'", 'symmetrical': 'False', 'to': u"orm['route.Node']"}),
            'visits': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['route.Node']", 'symmetrical': 'False'})
        },
        u'route.solution': {
            'Meta': {'object_name': 'Solution'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'route.solutionentry': {
            'Meta': {'object_name': 'SolutionEntry'},
            'end_seconds': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['route.Node']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['route.Solution']"}),
            'start_seconds': ('django.db.models.fields.FloatField', [], {}),
            'traveler': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'travelers'", 'to': u"orm['route.Node']"})
        }
    }

    complete_apps = ['route']