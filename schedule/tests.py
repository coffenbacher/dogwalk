from django.test import TestCase
from django.test.client import Client
from dog.models import *
from models import *

"""class ScheduleTest(TestCase):
    fixtures = ['walker.json', 'walkinglocations.json', 'dog.json', 'test.json']
    
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

"""
