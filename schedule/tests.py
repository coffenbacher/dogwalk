from django.test import TestCase
from dog.models import *
from models import *

class ScheduleTest(TestCase):
    fixtures = ['walker.json', 'walkinglocations.json', 'dog.json', 'test.json']
    
    def test_basic_schedule(self):
        w = Week()
        w.save()
        w.dogs = Dog.objects.all()
        w.walkers = Walker.objects.all()
        w.solve()
        
        w.choose_solution()
                

        w.schedule.entries_by_walker()
