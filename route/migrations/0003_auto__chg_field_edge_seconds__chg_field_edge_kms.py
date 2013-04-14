# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Edge.seconds'
        db.alter_column(u'route_edge', 'seconds', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Edge.kms'
        db.alter_column(u'route_edge', 'kms', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Edge.seconds'
        raise RuntimeError("Cannot reverse this migration. 'Edge.seconds' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Edge.kms'
        raise RuntimeError("Cannot reverse this migration. 'Edge.kms' and its values cannot be restored.")

    models = {
        u'route.edge': {
            'Meta': {'object_name': 'Edge'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kms': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['route.Node']", 'symmetrical': 'False'}),
            'seconds': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'route.node': {
            'Meta': {'object_name': 'Node'},
            'address': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nodes'", 'to': u"orm['route.Node']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['route.Solution']"}),
            'traveler': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'travelers'", 'to': u"orm['route.Node']"})
        }
    }

    complete_apps = ['route']