from django.test import TestCase
from django.test.client import Client
from dog.models import *
from models import *

class ScheduleTest(TestCase):
    fixtures = ['walker.json', 'walkinglocations.json', 'dog.json', 'test.json']
    
    #def setUp(self):
        #replace with test edges
        #Node.create_edges()

    """def test_basic_schedule(self):
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
        self.assertTrue(w.schedule.entries.count() > 40)"""

class ScheduleViewTest(TestCase):
    fixtures = ['schedule.json', 'scheduleentry.json']

    def setUp(self):
        self.client = Client()

    def test_view(self):
        response = self.client.get('/schedule/1/')
        self.failUnlessEqual(response.status_code, 200)
        json.loads(response.content)
    
    def test_map(self):
        response = self.client.get('/schedule/1/map/')
        self.failUnlessEqual(response.status_code, 200)


