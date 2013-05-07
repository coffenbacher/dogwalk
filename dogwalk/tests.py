import pdb
import dateutil.parser
from dog.models import *
from schedule.models import *
from graph.models import *

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from django.contrib.sites.models import Site
from dog.helpers import *
from urllib2 import urlopen
    
START = dateutil.parser.parse('2013-05-06')

class LoggedOutTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        User.objects.create_user(username='t@t.com', email='t@t.com', password='testests')

    def test_home(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 302)

class LoggedInTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        User.objects.create_user(username='t@t.com', email='t@t.com', password='testests')
        self.client.login(username='t@t.com', password='testests')

    def test_home(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_bootstrap(self):
        response = self.client.get('/static/bootstrap.css')
        self.failUnlessEqual(response.status_code, 200)


class OneDogTest(TestCase):
    fixtures = ['one_dog.json']

    def test_basic_solution(self):
        basic_solution(START)
        s = Solution.objects.all()[0]
        for d in s.pdogs.all():
            if not d.validate():
                print "%s FAILED" % d
        self.assertTrue(s.validate_dogs())


class SpacingTest(TestCase):
    fixtures = ['one_dog.json']
    def setUp(self):
        Dog.objects.filter(name='Alpha Dog').update(days=3)

    def test_days(self):
        basic_solution(START)
        self.assertTrue(Solution.objects.all()[0].validate_dogs())

    def test_spacing(self):
        basic_solution(START)
        for s in Event.objects.all():
            self.assertTrue(s.time.weekday() in [0, 2, 4])
    
class CancellationTest(TestCase):
    fixtures = ['one_dog.json']
    def setUp(self):
        CancelledWalk.objects.create(dog = Dog.objects.get(name='Alpha Dog'), date = dateutil.parser.parse('2013-05-07'))

    def test_days(self):
        Dog.objects.filter(name='Alpha Dog').update(days=5)
        basic_solution(START)
        self.assertTrue(Solution.objects.all()[0].validate_dogs())

    def test_5_day_cancellation(self):
        Dog.objects.filter(name='Alpha Dog').update(days=5)
        basic_solution(START)
        self.assertEquals(Event.objects.filter(time__gte=START, time__lte=START + datetime.timedelta(days=7)).count(), 4)
    
    def test_2_day_cancellation(self):
        Dog.objects.filter(name='Alpha Dog').update(days=2)
        basic_solution(START)
        self.assertEquals(Event.objects.filter(time__gte=START, time__lte=START + datetime.timedelta(days=7)).count(), 1)
    
    def test_1_day_cancellation(self):
        Dog.objects.filter(name='Alpha Dog').update(days=1)
        basic_solution(START)
        self.assertEquals(Event.objects.filter(time__gte=START, time__lte=START + datetime.timedelta(days=7)).count(), 0)

class TwPTest(TestCase):
    fixtures = ['initial_data.json', 'twp.json']
    
    def setUp(self):
        pass
    
    def test_basic_solution(self):
        basic_solution()
        s = Solution.objects.all()[0]
        for d in s.pdogs.all():
            if not d.validate():
                print "%s FAILED" % d
        self.assertTrue(s.validate_dogs())
