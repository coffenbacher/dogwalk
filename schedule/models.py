from django_extensions.db.models import TimeStampedModel
from dog.models import *
from route.models import *
from django.db import models

# Create your models here.

class Week(TimeStampedModel):
    walkers = models.ManyToManyField(Walker)
    dogs = models.ManyToManyField(Dog)
    problem = models.ForeignKey(Problem, null=True, blank=True)
    solutions = models.ManyToManyField(Solution, null=True, blank=True)
    schedule = models.ForeignKey('Schedule', null=True, blank=True)
    
    def solve(self):
        self.problem = Problem()
        self.problem.save()
        
        self.problem.start = [w.node for w in self.walkers.all()]
        self.problem.end = [WalkingLocation.objects.all()[0].node] #only works for one end
        self.problem.visits = [d.node for d in self.dogs.all()]

        s = self.problem.solve()
        self.solutions.add(s)
        
        return s
    
    def choose_solution(self):
        chosen = self.solutions.all()[0] # automatically pick first solution

        self.schedule = Schedule()
        self.schedule.save()

        for e in chosen.entries.all():
           self.schedule.entries.create(walker = e.traveler.walkers.all()[0], node = e.node) 

class Schedule(TimeStampedModel):
    pass

class ScheduleEntry(TimeStampedModel):
    walker = models.ForeignKey(Walker)
    node = models.ForeignKey(Node)
    schedule = models.ForeignKey(Schedule, related_name='entries')

