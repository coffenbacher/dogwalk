from django.db import models

# Create your models here.
class Problem(models.Model):
    start = models.ForeignKey('Node', related_name='starting_at')
    end = models.ForeignKey('Node', related_name='ending_at')
    visits = models.ManyToManyField('Node')

    
    #GREEDY ALGORITHM
    def solve(self):
        current = self.start
        v = list(self.visits.all())
        
        solution = [self.start]

        while v:
            closest_d = 99999
            
            for i in v:
                d = current.get_distance(i)
                if d < closest_d:
                    closest = i
                    closest_d = d
            
            current = closest
            v.remove(current)
            solution.append(current)

        solution.append(self.end)

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
