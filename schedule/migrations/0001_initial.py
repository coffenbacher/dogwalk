# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Week'
        db.create_table(u'schedule_week', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solver.Problem'], null=True, blank=True)),
            ('schedule', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['schedule.Schedule'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'schedule', ['Week'])

        # Adding M2M table for field walkers on 'Week'
        db.create_table(u'schedule_week_walkers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('week', models.ForeignKey(orm[u'schedule.week'], null=False)),
            ('walker', models.ForeignKey(orm[u'dog.walker'], null=False))
        ))
        db.create_unique(u'schedule_week_walkers', ['week_id', 'walker_id'])

        # Adding M2M table for field dogs on 'Week'
        db.create_table(u'schedule_week_dogs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('week', models.ForeignKey(orm[u'schedule.week'], null=False)),
            ('dog', models.ForeignKey(orm[u'dog.dog'], null=False))
        ))
        db.create_unique(u'schedule_week_dogs', ['week_id', 'dog_id'])

        # Adding M2M table for field solutions on 'Week'
        db.create_table(u'schedule_week_solutions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('week', models.ForeignKey(orm[u'schedule.week'], null=False)),
            ('solution', models.ForeignKey(orm[u'solver.solution'], null=False))
        ))
        db.create_unique(u'schedule_week_solutions', ['week_id', 'solution_id'])

        # Adding model 'Schedule'
        db.create_table(u'schedule_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'schedule', ['Schedule'])

        # Adding model 'ScheduleEntry'
        db.create_table(u'schedule_scheduleentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('walker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dog.Walker'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['schedule.Schedule'])),
        ))
        db.send_create_signal(u'schedule', ['ScheduleEntry'])


    def backwards(self, orm):
        # Deleting model 'Week'
        db.delete_table(u'schedule_week')

        # Removing M2M table for field walkers on 'Week'
        db.delete_table('schedule_week_walkers')

        # Removing M2M table for field dogs on 'Week'
        db.delete_table('schedule_week_dogs')

        # Removing M2M table for field solutions on 'Week'
        db.delete_table('schedule_week_solutions')

        # Deleting model 'Schedule'
        db.delete_table(u'schedule_schedule')

        # Deleting model 'ScheduleEntry'
        db.delete_table(u'schedule_scheduleentry')


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
        },
        u'schedule.schedule': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Schedule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        u'schedule.scheduleentry': {
            'Meta': {'ordering': "('pk',)", 'object_name': 'ScheduleEntry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['schedule.Schedule']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'walker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Walker']"})
        },
        u'schedule.week': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Week'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dogs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Dog']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['solver.Problem']", 'null': 'True', 'blank': 'True'}),
            'schedule': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['schedule.Schedule']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'solutions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['solver.Solution']", 'null': 'True', 'blank': 'True'}),
            'walkers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Walker']", 'symmetrical': 'False'})
        },
        u'solver.pdog': {
            'Meta': {'object_name': 'PDog'},
            'dog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Dog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'pwalker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carrying'", 'null': 'True', 'to': u"orm['solver.PWalker']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pdogs'", 'to': u"orm['solver.Solution']"}),
            'walked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'solver.problem': {
            'Meta': {'object_name': 'Problem'},
            'dogs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Dog']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_solution': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'main_problem'", 'unique': 'True', 'null': 'True', 'to': u"orm['solver.Solution']"}),
            'walkers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Walker']", 'symmetrical': 'False'}),
            'walkinglocations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.WalkingLocation']", 'symmetrical': 'False'})
        },
        u'solver.pwalker': {
            'Meta': {'object_name': 'PWalker'},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '9'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_entry': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'last_pwalker'", 'unique': 'True', 'null': 'True', 'to': u"orm['solver.SolutionEntry']"}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pwalkers'", 'to': u"orm['solver.Solution']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'walker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Walker']"})
        },
        u'solver.solution': {
            'Meta': {'object_name': 'Solution'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pending': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pending_pdogs'", 'symmetrical': 'False', 'to': u"orm['solver.PDog']"}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['solver.Problem']"})
        },
        u'solver.solutionentry': {
            'Meta': {'object_name': 'SolutionEntry'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'pwalker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['solver.PWalker']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['solver.Solution']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['schedule']