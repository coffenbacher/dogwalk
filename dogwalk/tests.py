import pdb
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

class BasicTest(TestCase):
    fixtures = ['hand.json']

    def test_basic_solution(self):
        basic_solution()
        s = Solution.objects.all()[0]
        for d in s.pdogs.all():
            if not d.validate():
                print "%s FAILED" % d
        self.assertTrue(s.validate_dogs())

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
