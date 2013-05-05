import pdb
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import *
from dog.helpers import basic_solution
from schedule.models import *
from models import *

class TwP_Helper_Test(TestCase):
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
    
"""class LoggedOutTest(TestCase):
    fixtures = ['initial_data.json', 'test.json']

    def setUp(self):
        self.client = Client()

    def test_list(self):
        response = self.client.get('/technique/')
        self.failUnlessEqual(response.status_code, 200)
    
    def test_create_GET(self):
        response = self.client.get('/technique/create/')
        self.failUnlessEqual(response.status_code, 302)

    def test_show(self):
        s = Technique.objects.all()[0]
        response = self.client.get('/technique/%s/' % s.pk)
        self.failUnlessEqual(response.status_code, 200)


class LoggedInTest(TestCase):
    fixtures = ['initial_data.json', 'test.json', 'test_users.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='test', password='test')
    
    def test_list(self):
        response = self.client.get('/technique/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertFalse('RelatedManager' in response.content)

    def test_create_youtube(self):
        t = Technique(name='test sub', type=TechniqueType.objects.all()[0], 
            level=Level.objects.all()[0], youtube_link='http://www.youtube.com/watch?v=lfiXMeyY15s',
            created_by=User.objects.all()[0])
        t.save()
        self.failUnlessEqual(t.youtube_id, 'lfiXMeyY15s')

    def test_create_GET(self):
        response = self.client.get('/technique/create/')
        self.assertTrue('Name' in response.content)
        self.assertTrue('Level' in response.content)
        self.assertTrue('Youtube' in response.content)
        self.failUnlessEqual(response.status_code, 200)
        
    def test_create_position_POST(self):
        d = {'type': 3, 'level': 1, 'name': 'Test Position', 'images-TOTAL_FORMS': 1, 'images-INITIAL_FORMS': 0, 'images-MAX_NUM_FORMS': '', 'images-0-image': '', 'images-0-id': '', 'images-0-DELETE': '', 'images-0-id': '', 'images-0-technique': ''}
        response = self.client.post('/technique/create/', d)
        self.failUnlessEqual(response.status_code, 302)
        self.assertTrue(Technique.objects.get(name='Test Position'))

    def test_create_incomplete_POST(self):
        d = {'type': '', 'level': 1, 'name': 'Test Incomplete', 'images-TOTAL_FORMS': 1, 'images-INITIAL_FORMS': 0, 'images-MAX_NUM_FORMS': '', 'images-0-image': '', 'images-0-id': '', 'images-0-DELETE': '', 'images-0-id': '', 'images-0-technique': ''}
        response = self.client.post('/technique/create/', d)
        self.failUnlessEqual(response.status_code, 200)
        self.assertFalse(Technique.objects.filter(name='Test Incomplete'))

    def test_edit_GET(self):
        s = Technique.objects.all()[0]
        response = self.client.get('/technique/%s/edit/' % s.pk)
        self.assertTrue(s.name in response.content)
        self.failUnlessEqual(response.status_code, 200)
    
    def test_edit_POST(self):
        s = Technique.objects.all()[0]
        self.assertTrue(s.level.pk == 1)

        d = {'type': 3, 'level': 2, 'name': 'Test Position2', 'images-TOTAL_FORMS': 1, 'images-INITIAL_FORMS': 0, 'images-MAX_NUM_FORMS': '', 'images-0-image': '', 'images-0-id': '', 'images-0-DELETE': '', 'images-0-id': '', 'images-0-technique': ''}
        
        response = self.client.post('/technique/%s/edit/' % s.pk, d)
        self.failUnlessEqual(response.status_code, 302)
        
        s = Technique.objects.get(pk=s.pk)
        self.assertTrue(s.level.pk == 2)"""
