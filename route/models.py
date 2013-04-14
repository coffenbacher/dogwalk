import urllib2
import json
from django.db import models

# Create your models here.
class Problem(models.Model):
    start = models.ManyToManyField('Node', related_name='starting_at')
    end = models.ManyToManyField('Node', related_name='ending_at')
    visits = models.ManyToManyField('Node')
    
    #GREEDY ALGORITHM
    def solve(self):
        v = list(self.visits.all())
        
        s = Solution()
        s.save()
        
        for traveler in self.start.all():
            s.entries.create(traveler = traveler, node = traveler)

        while v:
            for traveler in self.start.all():
                current = s.entries.filter(traveler=traveler).order_by('-pk')[0]
                closest_d = 999999999
            
                for i in v:
                    d = current.node.get_distance(i)
                    if d < closest_d:
                        closest = i
                        closest_d = d

                try:
                    v.remove(closest)
                    s.entries.create(traveler = traveler, node = closest)
                except:
                    print "ERROR"
                    pass

        for traveler in self.start.all():
            s.entries.create(traveler = traveler, node = self.end.all()[0])

        return s

class Node(models.Model):
    address = models.TextField()
    
    def create_edges(self):
        for n in Node.objects.all():
            if n != self and not Edge.objects.filter(nodes=self).filter(nodes=n):
                origin = urllib2.quote(self.address)
                destination = urllib2.quote(n.address)
                url = "http://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&sensor=false" % (origin, destination)
                req = urllib2.urlopen(url)
                route = json.loads(req.read())
                try:
                    seconds = route['routes'][0]['legs'][0]['duration']['value']
                    kms = route['routes'][0]['legs'][0]['distance']['value']
                    e = Edge.objects.create(kms = kms, seconds = seconds)
                    e.nodes = [n, self]
                except:
                    e = Edge.objects.create()
                    e.nodes = [n, self]


    def get_distance(self, n):
        e = Edge.objects.filter(nodes=self).filter(nodes=n)
        if not e:
            self.create_edges()
            e = Edge.objects.filter(nodes=self).filter(nodes=n)
        if not e[0].seconds:
            return 9999999999
        return e[0].seconds

    
    def __unicode__(self):
        return self.address

class Edge(models.Model):
    nodes = models.ManyToManyField(Node)
    kms = models.FloatField(null=True, blank=True)
    seconds = models.FloatField(null=True, blank=True)

class Solution(models.Model):
    pass

class SolutionEntry(models.Model):
    traveler = models.ForeignKey(Node, related_name='travelers')
    node = models.ForeignKey(Node, related_name='nodes')
    solution = models.ForeignKey(Solution, related_name='entries')
