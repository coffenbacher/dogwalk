import time
import pprint
import pdb
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
    
    @classmethod
    def create_edges(cls):
        nodes = list(Node.objects.all())
        
        P = 10 
        
        while nodes:
            origins = nodes[:P]
            for i in range(0, len(nodes), P):
                #print "working nodes %s:%s" % (i, i+P)
                destinations = nodes[i:i+P]
                #print "len(destinations) %s" % len(destinations)
                s_origins = [urllib2.quote(n.address) for n in origins]
                s_destinations = [urllib2.quote(n.address) for n in destinations]
                        
                url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&sensor=false" % ('|'.join(s_origins), '|'.join(s_destinations))
                #print url

                retry = 0
                incomplete = True
                while incomplete and retry < 3:
                    req = urllib2.urlopen(url)
                    res = json.loads(req.read())
                    pprint.pprint(res)
                    rows = res['rows']
                    pprint.pprint(rows)
                    if res['status'] == 'OK':
                        incomplete = False
                    else:
                        retry +=1 
                        time.sleep(5)

                for i in range(len(rows)):
                    row = rows[i]
                    o = origins[i]
                    
                    for j in range(len(row['elements'])):
                        e = row['elements'][j]
                        d = destinations[j]
                        #print o, d, e['distance']['value'], e['duration']['value']
                        if not Edge.objects.filter(nodes=o).filter(nodes=d) and d != o:
                            e = Edge.objects.create(meters = e['distance']['value'], seconds = e['duration']['value'])
                            e.nodes = [o, d]
                            e.save()
                            
                time.sleep(2)
           
            nodes = nodes[P-1:]     

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
    meters = models.FloatField(null=True, blank=True)
    seconds = models.FloatField(null=True, blank=True)

class Solution(models.Model):
    pass

class SolutionEntry(models.Model):
    traveler = models.ForeignKey(Node, related_name='travelers')
    node = models.ForeignKey(Node, related_name='nodes')
    solution = models.ForeignKey(Solution, related_name='entries')
