import datetime
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from models import *
from dog.models import *

class EdgeLoadingTest(TestCase):
    fixtures = ['initial_data.json', 'test.json']

    def setUp(self):
        Edge.objects.all().delete()

    def test_download_edges(self):
        self.failUnlessEqual(Node.objects.count(), 11)
        Node.create_edges()
        self.failUnlessEqual(Edge.objects.count(), 11*10/2)

class DesirableTimesTest(TestCase):
    def setUp(self):
        S = Walker.objects.create(name='S', address='test')
        T1 = Dog.objects.create(name='T1', days=3, address='1000 Olin Way')
        T2 = Dog.objects.create(name='T2', days=3, address='2000 Olin Way')
        R = RequiredWalk.objects.create(dog=T2, days=1,after='10:00:00', before='11:00:00')

        E = Edge.objects.create(seconds=1, meters=1)
        E.nodes = [S.node, T1.node]
        
        E2 = Edge.objects.create(seconds=1, meters=1)
        E2.nodes = [S.node, T2.node]

    def test_return_times_false(self):
        T1 = Dog.objects.get(name='T1')
        
        self.assertFalse(T1.node.get_desirable_times())
    
    def test_return_times_true(self):
        T2 = Dog.objects.get(name='T2')
        
        self.assertTrue(T2.node.get_desirable_times())

    def test_greedy(self):
        T1 = Dog.objects.get(name='T1')
        T2 = Dog.objects.get(name='T2')
        S = Walker.objects.get(name='S')
        
        n = S.node.get_closest_greedy([T1.node, T2.node])
        self.assertEquals(T1.node, n)

    def test_desirability(self):
        T1 = Dog.objects.get(name='T1')
        T2 = Dog.objects.get(name='T2')
        S = Walker.objects.get(name='S')
        
        n = S.node.get_best_greedy([T1.node, T2.node], datetime.datetime.strptime('10:15:00', '%H:%M:%S').time())
        self.assertEquals(T2.node, n)

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
