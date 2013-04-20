import datetime
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from models import *
from dog.models import *

class EdgeLoadingTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        Edge.objects.all().delete()

    def test_download_edges(self):
        N = 4
        self.failUnlessEqual(Node.objects.count(), N)
        Node.create_edges()
        self.failUnlessEqual(Edge.objects.count(), N*(N-1)/2)

class ProblemTest(TestCase):
    fixtures = ['test.json']
    def setUp(self):
        pass
