import pdb
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
