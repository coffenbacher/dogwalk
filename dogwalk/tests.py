import pdb
from dog.models import *
from schedule.models import *
from graph.models import *
from solver.models import *

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from django.contrib.sites.models import Site
from urllib2 import urlopen

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

class E2ETest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        walker = Walker.objects.create(name='Elizabeth', address='Boston, MA')
        wl = WalkingLocation.objects.create(address='Somerville, MA')

        d1 = Dog.objects.create(name='WellesleyDog', address='Wellesley, MA', days = 5)
        d2 = Dog.objects.create(name='NeedhamDog', address='Needham, MA', days = 1)
        
        e = Edge.objects.create(meters=1, seconds=1)
        e.nodes = [d1.node,d2.node]

        e = Edge.objects.create(meters=1, seconds=5)
        e.nodes = [d1.node,wl.node]

        e = Edge.objects.create(meters=1, seconds=10)
        e.nodes = [walker.node,d1.node]

        e = Edge.objects.create(meters=1, seconds=10)
        e.nodes = [walker.node,d2.node]

        e = Edge.objects.create(meters=1, seconds=10)
        e.nodes = [walker.node,wl.node]
        
        e = Edge.objects.create(meters=1, seconds=3)
        e.nodes = [wl.node,d2.node]

        w = Week.objects.create()
        w.dogs = [d1, d2]
        w.walkers = [walker]
        
        w.save()
        w.solve()
        w.choose_solution()
        
        self.assertEquals(w.schedule.entries.count(), 4)

class BastardTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        walker = Walker.objects.create(name='Elizabeth', address='Boston, MA')
        wl = WalkingLocation.objects.create(address='Somerville, MA')

        d1 = Dog.objects.create(name='WellesleyDog', address='Wellesley, MA', days = 5)
        d2 = Dog.objects.create(name='NeedhamDog', address='Needham, MA', days = 1)
        
        e = Edge.objects.create(meters=1, seconds=1)
        e.nodes = [d1.node,d2.node]

        e = Edge.objects.create(meters=1, seconds=5)
        e.nodes = [d1.node,wl.node]

        e = Edge.objects.create(meters=1, seconds=10)
        e.nodes = [walker.node,d1.node]

        e = Edge.objects.create(meters=1, seconds=10)
        e.nodes = [walker.node,d2.node]

        e = Edge.objects.create(meters=1, seconds=10)
        e.nodes = [walker.node,wl.node]
        
        e = Edge.objects.create(meters=1, seconds=3)
        e.nodes = [wl.node,d2.node]

        w = Week.objects.create()
        w.dogs = [d1, d2]
        w.walkers = [walker]
        
        w.save()
        w.solve()
        w.choose_solution()
        w.solve()
        w.choose_solution()
        w.save()
        
        self.assertEquals(w.schedule.entries.count(), 4)

