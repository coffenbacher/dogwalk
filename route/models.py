import time
import datetime
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
    
    #GREEDY ALGORITHM WITH TIME WEIGHTING
    def solve(self):
        v = list(self.visits.all())
        
        s = Solution()
        s.save()
        
        start_time = datetime.datetime.strptime('10:00:00', '%H:%M:%S')
        
        # ADD START POINT
        for traveler in self.start.all():
            s.entries.create(traveler = traveler, node = traveler, start_seconds=0)

        while v:
            # Take turns with the greedy algorithm choosing nodes
            for traveler in self.start.all():
                p = s.get_last_entry(traveler = traveler)
                
                t = (start_time + datetime.timedelta(seconds=p.end_seconds)).time()
                closest = traveler.traveler_get_best_greedy(s, v, t)
                
                edge = Edge.objects.filter(nodes=p.node).get(nodes=closest)
                s.entries.create(traveler = traveler, node = closest, start_seconds=p.end_seconds + edge.seconds)

                v.remove(closest)

        # ADD END POINT
        for traveler in self.start.all():
            p = s.entries.filter(traveler = traveler).order_by('-pk')[0]
            e = self.end.all()[0]
            edge = Edge.objects.filter(nodes=p.node).get(nodes=e)
            s.entries.create(traveler = traveler, node = e, start_seconds=p.end_seconds + edge.seconds)

        return s

class Node(models.Model):
    address = models.TextField()
    seconds = models.FloatField(default=420)
    
    def traveler_get_best_greedy(self, solution, nodes, t):
        p = solution.get_last_entry(traveler = self)
        n = p.node.get_best_greedy(nodes, t)
        if not n:
            raise Exception("Node finder failing to find an accessible node")
        return n    


    def traveler_get_closest_greedy(self, solution, nodes):
        p = solution.get_last_entry(traveler = self)
        return p.node.get_closest_greedy(nodes) 

    def get_best_greedy(self, nodes, t):
        for i in nodes:
            d = self.get_distance(i)
            #print self.address, i.address, d
            i.score = d
        
        for i in nodes:
            ts = i.get_desirable_times()
            for desirable in ts:
                #print desirable[0], t, desirable[1]
                if t > desirable[0] and t < desirable[1]:
                    i.score -= 10000 # configure eventually
        
        #DEBUG
        #for i in nodes:
        #    print i.score

        #Lower score is better!
        return sorted(nodes, key=lambda n: n.score)[0]

    def get_closest_greedy(self, nodes):
        closest_d = 999999999 # impossibly high

        for i in nodes:
            d = self.get_distance(i)
            if d < closest_d:
                closest = i
                closest_d = d
        
        return closest

    def get_desirable_times(self):
        if hasattr(self, 'dog'):
            return [(rw.after, rw.before) for rw in self.dog.requiredwalks.all()]
        
        return False    


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
                    rows = res['rows']
                    if res['status'] == 'OK':
                        incomplete = False
                    else:
                        pprint.pprint(res)
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
                            
                time.sleep(3)
           
            nodes = nodes[P-1:]     

    def get_distance(self, n):
        e = Edge.objects.filter(nodes=self).get(nodes=n)
        return e.seconds

    
    def __unicode__(self):
        return self.address

class Edge(models.Model):
    nodes = models.ManyToManyField(Node)
    meters = models.FloatField(null=True, blank=True)
    seconds = models.FloatField(null=True, blank=True)

class Solution(models.Model):
    def get_last_entry(self, traveler):
        return self.entries.filter(traveler = traveler).order_by('-pk')[0]

class SolutionEntry(models.Model):
    traveler = models.ForeignKey(Node, related_name='travelers')
    node = models.ForeignKey(Node, related_name='nodes')
    solution = models.ForeignKey(Solution, related_name='entries')
    start_seconds = models.FloatField()
    end_seconds = models.FloatField()
    
    def save(self, *args, **kwargs):
        self.end_seconds = self.start_seconds + self.node.seconds

        return super(SolutionEntry, self).save(*args, **kwargs)
