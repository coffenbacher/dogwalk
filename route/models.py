from django.db import models

# Create your models here.
class Problem(models.Model):
    start = models.ManyToManyField('Node', related_name='starting_at')
    end = models.ManyToManyField('Node', related_name='ending_at')
    visits = models.ManyToManyField('Node')
    
    #GREEDY ALGORITHM
    def solve(self):
        v = list(self.visits.all())
        
        solution = {}
        for traveler in self.start.all():
            solution[traveler] = [traveler]

        while v:
            for traveler in self.start.all():
                closest_d = 99999
            
                for i in v:
                    d = solution[traveler][-1].get_distance(i)
                    if d < closest_d:
                        closest = i
                        closest_d = d
            
                next_node = closest
                v.remove(next_node)
                solution[traveler].append(next_node)

        for traveler in self.start.all():
            solution[traveler].append(self.end.all()[0]) # only works for one end node

        return solution

class Node(models.Model):
    address = models.TextField()
    
    def get_distance(self, n):
        return Edge.objects.filter(nodes__in=(self, n))[0].minutes
    
    def __unicode__(self):
        return self.address

class Edge(models.Model):
    nodes = models.ManyToManyField(Node)
    miles = models.FloatField()
    minutes = models.FloatField()
