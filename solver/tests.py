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
    

class Solution_MultiDay_Test(TestCase):
    fixtures = ['walker_test.json', 'dog_test.json', 'walkinglocation_test.json', 'edge_test.json']
    def setUp(self):
        p = Problem.objects.create()
        p.walkers = Walker.objects.all()
        p.dogs = Dog.objects.all()
        p.dogs.update(days = 2)
        p.walkinglocations = WalkingLocation.objects.all()
        p.save()
        self.solution = p.solution_set.all()[0]
        self.problem = p

    def test_solve(self):
        sol = self.problem.solve()
        self.assertTrue(sol.entries.count() > 30)
        self.assertTrue(sol.entries.order_by('-end')[0].end.day > 5)
        print sol.entries

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
