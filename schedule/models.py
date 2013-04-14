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
    schedule = models.OneToOneField('Schedule', null=True, blank=True)
    
    def solve(self):
        self.problem = Problem()
        self.problem.save()
        
        self.problem.start = [w.node for w in self.walkers.all()]
        self.problem.end = [WalkingLocation.objects.all()[0].node] #only works for one end
        self.problem.visits = [d.node for d in self.dogs.all()]

        s = self.problem.solve()
        self.solutions.add(s)
        
        return s
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super(Week, self).save(*args, **kwargs)
            self.solve()
            self.choose_solution()

        super(Week, self).save(*args, **kwargs)
        
    def choose_solution(self):
        chosen = self.solutions.all()[0] # automatically pick first solution

        s = Schedule()
        s.save()

        for e in chosen.entries.all():
           s.entries.create(walker = e.traveler.walkers.all()[0], node = e.node) 
        
        s.save()
        
        self.schedule = s
        self.save()

class Schedule(TimeStampedModel):
    def entries_by_walker(self):
        res = []
        for w in self.week.walkers.all():
            res.append([w, self.entries.filter(walker=w)])
        return res

class ScheduleEntry(TimeStampedModel):
    class Meta:
        ordering = ('pk',)
        
    walker = models.ForeignKey(Walker)
    node = models.ForeignKey(Node)
    schedule = models.ForeignKey(Schedule, related_name='entries')

