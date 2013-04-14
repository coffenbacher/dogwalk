import pdb
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from django.contrib.sites.models import Site
from urllib2 import urlopen

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_bootstrap(self):
        response = self.client.get('/static/bootstrap.css')
        self.failUnlessEqual(response.status_code, 200)
