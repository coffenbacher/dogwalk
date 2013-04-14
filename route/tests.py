import pdb
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from models import *

class GreedyRouteFindingTest(TestCase):
    fixtures = ['initial_data.json', 'test.json']

    def setUp(self):
        pass

    def test_solver_basic(self):
        p = Problem.objects.create()
        p.save()
        p.start = Node.objects.filter(id=1)
        p.end = Node.objects.filter(id=3)
        p.visits = Node.objects.filter(id=2)
        routes = p.solve()
        
        optimal = {
            Node.objects.get(id=1) : [ Node.objects.get(pk=1),
                                        Node.objects.get(pk=2),
                                        Node.objects.get(pk=3)
                                        ]
                    }
        self.failUnlessEqual(routes, optimal)
   
    def test_solver_basic4(self):
        p = Problem.objects.create()
        p.save()
        p.start = Node.objects.filter(id=1)
        p.end = Node.objects.filter(id=4)
        p.visits = Node.objects.filter(id__in=(3,2)).order_by('-pk')
        routes = p.solve()
        
        optimal = {
            Node.objects.get(id=1) : [ Node.objects.get(pk=1),
                                        Node.objects.get(pk=2),
                                        Node.objects.get(pk=3),
                                        Node.objects.get(pk=4)
                                        ]
                    }
        self.failUnlessEqual(routes, optimal)
   
    def test_solver_multiple_start(self):
        p = Problem.objects.create()
        p.save()
        p.start = Node.objects.filter(id__in=(1,4))
        p.end = Node.objects.filter(id=4)
        p.visits = Node.objects.filter(id__in=(3,2)).order_by('-pk')
        routes = p.solve()
        
        optimal = {
            Node.objects.get(id=1) : [ Node.objects.get(pk=1),
                                        Node.objects.get(pk=2),
                                        Node.objects.get(pk=4)
                                        ],
            Node.objects.get(id=4) : [ Node.objects.get(pk=4),
                                        Node.objects.get(pk=3),
                                        Node.objects.get(pk=4)
                                        ]
                    }
        self.failUnlessEqual(routes, optimal)
