from django.test import TestCase
from django.test.client import Client
from dog.models import *
from models import *

class ScheduleTest(TestCase):
    fixtures = ['test.json']
    
    def setUp(self):
        self.s = Schedule(start='2013-01-01', end='2013-04-01')
        self.s.save()
    
    def test_compile(self):
        return True
    
    def test_save(self):    
        self.s.walkers = Walker.objects.all()
        self.s.dogs = Dog.objects.all()
        self.s.save()
        
        solution = self.s.solutions.all()[0]
        self.assertTrue(solution.pwalkers.all())
        self.assertTrue(solution.pdogs.all())
        
