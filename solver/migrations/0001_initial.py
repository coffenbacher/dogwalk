# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Problem'
        db.create_table(u'solver_problem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('main_solution', self.gf('django.db.models.fields.related.OneToOneField')(related_name='main_problem', unique=True, null=True, to=orm['solver.Solution'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 1, 0, 0))),
        ))
        db.send_create_signal(u'solver', ['Problem'])

        # Adding M2M table for field walkers on 'Problem'
        db.create_table(u'solver_problem_walkers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('problem', models.ForeignKey(orm[u'solver.problem'], null=False)),
            ('walker', models.ForeignKey(orm[u'dog.walker'], null=False))
        ))
        db.create_unique(u'solver_problem_walkers', ['problem_id', 'walker_id'])

        # Adding M2M table for field dogs on 'Problem'
        db.create_table(u'solver_problem_dogs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('problem', models.ForeignKey(orm[u'solver.problem'], null=False)),
            ('dog', models.ForeignKey(orm[u'dog.dog'], null=False))
        ))
        db.create_unique(u'solver_problem_dogs', ['problem_id', 'dog_id'])

        # Adding M2M table for field walkinglocations on 'Problem'
        db.create_table(u'solver_problem_walkinglocations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('problem', models.ForeignKey(orm[u'solver.problem'], null=False)),
            ('walkinglocation', models.ForeignKey(orm[u'dog.walkinglocation'], null=False))
        ))
        db.create_unique(u'solver_problem_walkinglocations', ['problem_id', 'walkinglocation_id'])

        # Adding model 'Solution'
        db.create_table(u'solver_solution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solver.Problem'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'solver', ['Solution'])

        # Adding model 'SolutionEntry'
        db.create_table(u'solver_solutionentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['solver.Solution'])),
            ('pwalker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['solver.PWalker'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'solver', ['SolutionEntry'])

        # Adding model 'PWalker'
        db.create_table(u'solver_pwalker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pwalkers', to=orm['solver.Solution'])),
            ('walker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dog.Walker'])),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')(default=9)),
            ('last_entry', self.gf('django.db.models.fields.related.OneToOneField')(related_name='last_pwalker', unique=True, null=True, to=orm['solver.SolutionEntry'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'solver', ['PWalker'])

        # Adding model 'PDog'
        db.create_table(u'solver_pdog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dog.Dog'])),
            ('solution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dogs', to=orm['solver.Solution'])),
            ('pwalker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='carrying', null=True, to=orm['solver.PWalker'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graph.Node'])),
            ('walked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('carried', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'solver', ['PDog'])


    def backwards(self, orm):
        # Deleting model 'Problem'
        db.delete_table(u'solver_problem')

        # Removing M2M table for field walkers on 'Problem'
        db.delete_table('solver_problem_walkers')

        # Removing M2M table for field dogs on 'Problem'
        db.delete_table('solver_problem_dogs')

        # Removing M2M table for field walkinglocations on 'Problem'
        db.delete_table('solver_problem_walkinglocations')

        # Deleting model 'Solution'
        db.delete_table(u'solver_solution')

        # Deleting model 'SolutionEntry'
        db.delete_table(u'solver_solutionentry')

        # Deleting model 'PWalker'
        db.delete_table(u'solver_pwalker')

        # Deleting model 'PDog'
        db.delete_table(u'solver_pdog')


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
        u'solver.pdog': {
            'Meta': {'object_name': 'PDog'},
            'carried': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dog.Dog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graph.Node']"}),
            'pwalker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'carrying'", 'null': 'True', 'to': u"orm['solver.PWalker']"}),
            'solution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dogs'", 'to': u"orm['solver.Solution']"}),
            'walked': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'solver.problem': {
            'Meta': {'object_name': 'Problem'},
            'dogs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dog.Dog']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_solution': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'main_problem'", 'unique': 'True', 'null': 'True', 'to': u"orm['solver.Solution']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 1, 0, 0)'}),
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
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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

    complete_apps = ['solver']