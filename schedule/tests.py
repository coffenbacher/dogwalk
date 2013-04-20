from django.test import TestCase
from dog.models import *
from models import *

class ScheduleTest(TestCase):
    fixtures = ['walker.json', 'walkinglocations.json', 'dog.json', 'test.json']
    
    def setUp(self):
        Node.create_edges()

    def test_basic_schedule(self):
        w = Week()
        w.save()
        w.dogs = Dog.objects.all()
        w.walkers = Walker.objects.all()
        w.solve()
        w.choose_solution()
        w.schedule.entries_by_walker()
        
        self.assertTrue(w.schedule)
        self.assertTrue(w.solutions.all())
        
        s = w.solutions.all()[0]
        
        print s.entries.all()
        
        self.assertTrue(s.entries.count() > 5)
        self.assertTrue(w.schedule.entries.count() > 5)

    def test_multiday_schedule(self):
        # dogs need to be walked all 5 days
        w = Week()
        w.save()
        w.dogs = Dog.objects.all()
        w.dogs.update(days=5)
        w.walkers = Walker.objects.all()
        w.solve()
        w.choose_solution()
        w.schedule.entries_by_walker()
        
        self.assertTrue(w.schedule)
        self.assertTrue(w.solutions.all())
        
        s = w.solutions.all()[0]
        
        print s.entries.all()
        
        self.assertTrue(s.entries.count() > 40)
        self.assertTrue(w.schedule.entries.count() > 40)

