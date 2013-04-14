# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NodeLocation'
        db.create_table(u'route_nodelocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'route', ['NodeLocation'])

        # Adding model 'DistanceEdge'
        db.create_table(u'route_distanceedge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('miles', self.gf('django.db.models.fields.FloatField')()),
            ('minutes', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'route', ['DistanceEdge'])

        # Adding M2M table for field locations on 'DistanceEdge'
        db.create_table(u'route_distanceedge_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('distanceedge', models.ForeignKey(orm[u'route.distanceedge'], null=False)),
            ('nodelocation', models.ForeignKey(orm[u'route.nodelocation'], null=False))
        ))
        db.create_unique(u'route_distanceedge_locations', ['distanceedge_id', 'nodelocation_id'])


    def backwards(self, orm):
        # Deleting model 'NodeLocation'
        db.delete_table(u'route_nodelocation')

        # Deleting model 'DistanceEdge'
        db.delete_table(u'route_distanceedge')

        # Removing M2M table for field locations on 'DistanceEdge'
        db.delete_table('route_distanceedge_locations')


    models = {
        u'route.distanceedge': {
            'Meta': {'object_name': 'DistanceEdge'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['route.NodeLocation']", 'symmetrical': 'False'}),
            'miles': ('django.db.models.fields.FloatField', [], {}),
            'minutes': ('django.db.models.fields.FloatField', [], {})
        },
        u'route.nodelocation': {
            'Meta': {'object_name': 'NodeLocation'},
            'address': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['route']