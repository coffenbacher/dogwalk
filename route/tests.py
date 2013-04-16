from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from models import *

class EdgeLoadingTest(TestCase):
    fixtures = ['initial_data.json', 'test.json']

    def setUp(self):
        Edge.objects.all().delete()

    def test_download_edges(self):
        self.failUnlessEqual(Node.objects.count(), 11)
        Node.create_edges()
        self.failUnlessEqual(Edge.objects.count(), 11*10/2)

class GreedyRouteFindingTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        pass

    def test_solver_basic(self):
        p = Problem.objects.create()
        p.save()
        p.start = Node.objects.filter(id=1)
        p.end = Node.objects.filter(id=3)
        p.visits = Node.objects.filter(id=2)
        s = p.solve()
        
        o = Solution()
        o.save()
        t = p.start.all()[0]
        o.entries.create(traveler=t,node = Node.objects.get(pk=1), start_seconds=0)
        o.entries.create(traveler=t,node = Node.objects.get(pk=2), start_seconds=0) 
        o.entries.create(traveler=t,node = Node.objects.get(pk=3), start_seconds=0) 
        
        for i in range(o.entries.count()):
            self.failUnlessEqual(s.entries.all()[i].traveler, o.entries.all()[i].traveler)
            self.failUnlessEqual(s.entries.all()[i].node, o.entries.all()[i].node)
   
    def test_solver_basic4(self):
        p = Problem.objects.create()
        p.save()
        p.start = Node.objects.filter(id=1)
        p.end = Node.objects.filter(id=4)
        p.visits = Node.objects.filter(id__in=(3,2)).order_by('-pk')
        s = p.solve()
        
        o = Solution()
        o.save()
        t = p.start.all()[0]
        o.entries.create(traveler=t,node = Node.objects.get(pk=1), start_seconds=0)
        o.entries.create(traveler=t,node = Node.objects.get(pk=2), start_seconds=0) 
        o.entries.create(traveler=t,node = Node.objects.get(pk=3), start_seconds=0) 
        o.entries.create(traveler=t,node = Node.objects.get(pk=4), start_seconds=0) 
        
        for i in range(o.entries.count()):
            self.failUnlessEqual(s.entries.all()[i].traveler, o.entries.all()[i].traveler)
            self.failUnlessEqual(s.entries.all()[i].node, o.entries.all()[i].node)
    
    def test_solver_multiple_start(self):
        p = Problem.objects.create()
        p.save()
        p.start = Node.objects.filter(id__in=(1,4))
        p.end = Node.objects.filter(id=4)
        p.visits = Node.objects.filter(id__in=(3,2)).order_by('-pk')
        s = p.solve()
        
        o = Solution()
        o.save()
        t = p.start.all()[0]
        t1 = p.start.all()[1]
        o.entries.create(traveler=t,node = Node.objects.get(pk=1), start_seconds=0)
        o.entries.create(traveler=t1,node = Node.objects.get(pk=4), start_seconds=0)
        o.entries.create(traveler=t,node = Node.objects.get(pk=2), start_seconds=421) 
        o.entries.create(traveler=t1,node = Node.objects.get(pk=3), start_seconds=430) 
        o.entries.create(traveler=t,node = Node.objects.get(pk=4), start_seconds=852) 
        o.entries.create(traveler=t1,node = Node.objects.get(pk=4), start_seconds=860) 
        
        for i in range(o.entries.count()):
            self.failUnlessEqual(s.entries.all()[i].traveler, o.entries.all()[i].traveler)
            self.failUnlessEqual(s.entries.all()[i].node, o.entries.all()[i].node)
            self.failUnlessEqual(s.entries.all()[i].start_seconds, o.entries.all()[i].start_seconds)
