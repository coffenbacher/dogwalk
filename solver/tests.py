import datetime
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from models import *
from dog.models import *

class ProblemTest(TestCase):
    fixtures = ['walker_test.json', 'dog_test.json', 'walkinglocation_test.json', 'edge_test.json']
    def setUp(self):
        self.p = Problem.objects.create()
        self.p.walkers = Walker.objects.all()
        self.p.dogs = Dog.objects.all()
        self.p.walkinglocations = WalkingLocation.objects.all()
        self.p.save()

    def test_creation(self):
        self.assertTrue(self.p.dogs.all())
    
    def test_solve(self):
        self.assertTrue(self.p.solve())
        self.assertTrue(SolutionEntry.objects.count() > 0)
    
class SolutionTest(TestCase):
    fixtures = ['walker_test.json', 'dog_test.json', 'walkinglocation_test.json', 'edge_test.json']
    def setUp(self):
        p = Problem.objects.create()
        p.walkers = Walker.objects.all()
        p.dogs = Dog.objects.all()
        p.walkinglocations = WalkingLocation.objects.all()
        p.save()
        self.solution = p.solution_set.all()[0]

    def test_creation(self):
        self.assertTrue(self.solution.problem.dogs.all())
        self.assertTrue(PDog.objects.all())
        self.assertEquals(PDog.objects.count(), self.solution.pdogs.count())
        
    def test_solved(self):
        self.solution.pending = []
        self.assertTrue(self.solution.solved())
    
    def test_solved_false(self):
        self.solution.pending = PDog.objects.all()
        self.assertFalse(self.solution.solved())

class SolutionEntryTest(TestCase):
    pass

class PWalkerTest(TestCase):
    fixtures = ['walker_test.json', 'dog_test.json', 'walkinglocation_test.json', 'edge_test.json']
    def setUp(self):
        p = Problem.objects.create()
        p.walkers = Walker.objects.all()
        p.dogs = Dog.objects.all()
        p.walkinglocations = WalkingLocation.objects.all()
        p.save()

        self.pwalker = p.solution_set.all()[0].pwalkers.all()[0]
   
    def test_creation(self):
        pass

    def test_turn(self):
        self.pwalker.turn()

class PDogTest(TestCase):
    pass
