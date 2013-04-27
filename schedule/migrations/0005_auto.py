# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field walkinglocations on 'Schedule'
        db.create_table(u'schedule_schedule_walkinglocations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm[u'schedule.schedule'], null=False)),
            ('walkinglocation', models.ForeignKey(orm[u'dog.walkinglocation'], null=False))
        ))
        db.create_unique(u'schedule_schedule_walkinglocations', ['schedule_id', 'walkinglocation_id'])


    def backwards(self, orm):
        # Removing M2M table for field walkinglocations on 'Schedule'
        db.delete_table('schedule_schedule_walkinglocations')


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
        u'dog.walker': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Walker'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'default': "'15:00:00'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'walkers'", 'to': u"orm['graph.Node']"}),
            'start_time': ('django.db.models.fields.TimeField', [], {'default': "'10:00:00'"})
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
        },
        u'schedule.event': {
            'Meta': {'object_name': 'Event'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pdog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': u"orm['schedule.PDog']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'schedule.pdog': {
            'Meta': {'object_name': 'PDog'},
            'carried': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Dog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'pwalker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carrying'", 'null': 'True', 'to': u"orm['schedule.PWalker']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pdogs'", 'to': u"orm['schedule.Solution']"}),
            'walked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'schedule.pwalker': {
            'Meta': {'object_name': 'PWalker'},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_entry': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'last_pwalker'", 'unique': 'True', 'null': 'True', 'to': u"orm['schedule.SolutionEntry']"}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pwalkers'", 'to': u"orm['schedule.Solution']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'walker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Walker']"})
        },
        u'schedule.schedule': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Schedule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dogs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Dog']", 'symmetrical': 'False'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_solution': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'main_schedule'", 'null': 'True', 'to': u"orm['schedule.Solution']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'walkers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Walker']", 'symmetrical': 'False'}),
            'walkinglocations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.WalkingLocation']", 'symmetrical': 'False'})
        },
        u'schedule.solution': {
            'Meta': {'object_name': 'Solution'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'solutions'", 'to': u"orm['schedule.Schedule']"})
        },
        u'schedule.solutionentry': {
            'Meta': {'object_name': 'SolutionEntry'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'pwalker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedule.PWalker']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['schedule.Solution']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['schedule']