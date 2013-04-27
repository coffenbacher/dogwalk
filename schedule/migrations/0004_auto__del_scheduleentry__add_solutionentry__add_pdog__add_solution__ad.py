# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ScheduleEntry'
        db.delete_table(u'schedule_scheduleentry')

        # Adding model 'SolutionEntry'
        db.create_table(u'schedule_solutionentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['schedule.Solution'])),
            ('pwalker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.PWalker'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'schedule', ['SolutionEntry'])

        # Adding model 'PDog'
        db.create_table(u'schedule_pdog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dog.Dog'])),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pdogs', to=orm['schedule.Solution'])),
            ('pwalker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carrying', null=True, to=orm['schedule.PWalker'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('walked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('carried', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'schedule', ['PDog'])

        # Adding model 'Solution'
        db.create_table(u'schedule_solution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='solutions', to=orm['schedule.Schedule'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'schedule', ['Solution'])

        # Adding model 'PWalker'
        db.create_table(u'schedule_pwalker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pwalkers', to=orm['schedule.Solution'])),
            ('walker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dog.Walker'])),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')(default=9)),
            ('last_entry', self.gf('django.db.models.fields.related.OneToOneField')(related_name='last_pwalker', unique=True, null=True, to=orm['schedule.SolutionEntry'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'schedule', ['PWalker'])

        # Adding model 'Event'
        db.create_table(u'schedule_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pdog', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['schedule.PDog'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'schedule', ['Event'])

        # Deleting field 'Schedule.problem'
        db.delete_column(u'schedule_schedule', 'problem_id')

        # Adding field 'Schedule.main_solution'
        db.add_column(u'schedule_schedule', 'main_solution',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='main_schedule', null=True, to=orm['schedule.Solution']),
                      keep_default=False)

        # Removing M2M table for field solutions on 'Schedule'
        db.delete_table('schedule_schedule_solutions')


    def backwards(self, orm):
        # Adding model 'ScheduleEntry'
        db.create_table(u'schedule_scheduleentry', (
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('walker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dog.Walker'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['schedule.Schedule'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'schedule', ['ScheduleEntry'])

        # Deleting model 'SolutionEntry'
        db.delete_table(u'schedule_solutionentry')

        # Deleting model 'PDog'
        db.delete_table(u'schedule_pdog')

        # Deleting model 'Solution'
        db.delete_table(u'schedule_solution')

        # Deleting model 'PWalker'
        db.delete_table(u'schedule_pwalker')

        # Deleting model 'Event'
        db.delete_table(u'schedule_event')

        # Adding field 'Schedule.problem'
        db.add_column(u'schedule_schedule', 'problem',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solver.Problem'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Schedule.main_solution'
        db.delete_column(u'schedule_schedule', 'main_solution_id')

        # Adding M2M table for field solutions on 'Schedule'
        db.create_table(u'schedule_schedule_solutions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm[u'schedule.schedule'], null=False)),
            ('solution', models.ForeignKey(orm[u'solver.solution'], null=False))
        ))
        db.create_unique(u'schedule_schedule_solutions', ['schedule_id', 'solution_id'])


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
            'walkers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Walker']", 'symmetrical': 'False'})
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