# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Solution'
        db.create_table(u'route_solution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'route', ['Solution'])

        # Adding model 'SolutionEntry'
        db.create_table(u'route_solutionentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('traveler', self.gf('django.db.models.fields.related.ForeignKey')(related_name='travelers', to=orm['route.Node'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nodes', to=orm['route.Node'])),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['route.Solution'])),
        ))
        db.send_create_signal(u'route', ['SolutionEntry'])

        # Deleting field 'Edge.miles'
        db.delete_column(u'route_edge', 'miles')

        # Deleting field 'Edge.minutes'
        db.delete_column(u'route_edge', 'minutes')

        # Adding field 'Edge.kms'
        db.add_column(u'route_edge', 'kms',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Edge.seconds'
        db.add_column(u'route_edge', 'seconds',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Solution'
        db.delete_table(u'route_solution')

        # Deleting model 'SolutionEntry'
        db.delete_table(u'route_solutionentry')


        # User chose to not deal with backwards NULL issues for 'Edge.miles'
        raise RuntimeError("Cannot reverse this migration. 'Edge.miles' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Edge.minutes'
        raise RuntimeError("Cannot reverse this migration. 'Edge.minutes' and its values cannot be restored.")
        # Deleting field 'Edge.kms'
        db.delete_column(u'route_edge', 'kms')

        # Deleting field 'Edge.seconds'
        db.delete_column(u'route_edge', 'seconds')


    models = {
        u'route.edge': {
            'Meta': {'object_name': 'Edge'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kms': ('django.db.models.fields.FloatField', [], {}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['route.Node']", 'symmetrical': 'False'}),
            'seconds': ('django.db.models.fields.FloatField', [], {})
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