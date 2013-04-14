# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Problem'
        db.create_table(u'route_problem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='starting_at', to=orm['route.Node'])),
            ('end', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ending_at', to=orm['route.Node'])),
        ))
        db.send_create_signal(u'route', ['Problem'])

        # Adding M2M table for field visits on 'Problem'
        db.create_table(u'route_problem_visits', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('problem', models.ForeignKey(orm[u'route.problem'], null=False)),
            ('node', models.ForeignKey(orm[u'route.node'], null=False))
        ))
        db.create_unique(u'route_problem_visits', ['problem_id', 'node_id'])

        # Adding model 'Node'
        db.create_table(u'route_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'route', ['Node'])

        # Adding model 'Edge'
        db.create_table(u'route_edge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('miles', self.gf('django.db.models.fields.FloatField')()),
            ('minutes', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'route', ['Edge'])

        # Adding M2M table for field nodes on 'Edge'
        db.create_table(u'route_edge_nodes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('edge', models.ForeignKey(orm[u'route.edge'], null=False)),
            ('node', models.ForeignKey(orm[u'route.node'], null=False))
        ))
        db.create_unique(u'route_edge_nodes', ['edge_id', 'node_id'])


    def backwards(self, orm):
        # Deleting model 'Problem'
        db.delete_table(u'route_problem')

        # Removing M2M table for field visits on 'Problem'
        db.delete_table('route_problem_visits')

        # Deleting model 'Node'
        db.delete_table(u'route_node')

        # Deleting model 'Edge'
        db.delete_table(u'route_edge')

        # Removing M2M table for field nodes on 'Edge'
        db.delete_table('route_edge_nodes')


    models = {
        u'route.edge': {
            'Meta': {'object_name': 'Edge'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'miles': ('django.db.models.fields.FloatField', [], {}),
            'minutes': ('django.db.models.fields.FloatField', [], {}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['route.Node']", 'symmetrical': 'False'})
        },
        u'route.node': {
            'Meta': {'object_name': 'Node'},
            'address': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'route.problem': {
            'Meta': {'object_name': 'Problem'},
            'end': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ending_at'", 'to': u"orm['route.Node']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'starting_at'", 'to': u"orm['route.Node']"}),
            'visits': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['route.Node']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['route']