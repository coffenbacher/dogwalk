import time
import json
import pprint
import urllib2
from django.db import models

class Edge(models.Model):
    nodes = models.ManyToManyField('Node')
    meters = models.FloatField(null=True, blank=True)
    seconds = models.FloatField(null=True, blank=True)

class Node(models.Model):
    address = models.TextField()
    seconds = models.FloatField(default=420)

    @classmethod
    def create_edges(cls):
        nodes = list(Node.objects.all())
        
        P = 10 
        
        while nodes:
            print 'Remaining: %s' % len(nodes)
            origins = nodes[:P]
            for i in range(0, len(nodes), P):
                print "working nodes %s:%s out of %s" % (i, i+P, len(nodes))
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
                        time.sleep(10)

                for i in range(len(rows)):
                    row = rows[i]
                    o = origins[i]
                    
                    for j in range(len(row['elements'])):
                        e = row['elements'][j]
                        d = destinations[j]
                        print o, d, e['distance']['value'], e['duration']['value']
                        if not Edge.objects.filter(nodes=o).filter(nodes=d) and d != o:
                            e = Edge.objects.create(meters = e['distance']['value'], seconds = e['duration']['value'])
                            e.nodes = [o, d]
                            e.save()
                            
                time.sleep(11)
           
            nodes = nodes[P-1:]     

    def get_distance(self, n):
        if self == n:
            return 0
        e = Edge.objects.filter(nodes=self).get(nodes=n)
        return e.seconds
    
    def __unicode__(self):
        return self.address
