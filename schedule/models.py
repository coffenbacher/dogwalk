import datetime
from django_extensions.db.models import TimeStampedModel
from dog.models import *
from graph.models import *
from solver.models import *
from django.db import models

# Create your models here.
DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
        )

class Schedule(TimeStampedModel):
    walkers = models.ManyToManyField(Walker)
    dogs = models.ManyToManyField(Dog)
    problem = models.ForeignKey(Problem, null=True, blank=True)
    solutions = models.ManyToManyField(Solution, null=True, blank=True)
    start = models.DateField()
    end = models.DateField()
    
    def solve(self):
        self.problem = Problem(start_date = self.start, end_date = self.end)
        self.problem.save()
        
        self.problem.walkers = self.walkers.all()
        self.problem.dogs = self.dogs.all()
        self.problem.walkinglocations = WalkingLocation.objects.all()
        self.problem.save()

        s = self.problem.solve()
        self.solutions.add(s)
        
        return s
    
    def choose_solution(self):
        chosen = self.solutions.all()[0] # automatically pick first solution

        d1 = datetime.datetime.strptime("10:00:00", "%H:%M:%S")
        for e in chosen.entries.all():
           self.entries.create(walker = e.pwalker.walker,
                                node = e.node,  
                                start = e.start,
                                end = e.end,
                                action = e.action) 
        
        self.save()

    def entries_by_walker(self):
        res = []
        for w in self.walkers.all():
            res.append([w, self.entries.filter(walker=w)])
        return res
    
    def entries_by_day(self):
        
        entries = self.entries.all()
        days = entries.dates('start', 'day')

        res = []
        for d in days:
            res.append([d, self.entries.filter(start__day = d.day).order_by('walker', 'start')])
            
        return res
    
    def entries_by_dog(self):
        res = []
        for d in self.dogs.all():
            res.append([d, self.entries.filter(node=d.node).order_by('start')])
        return res
        
    #def status_by_dog(self):
    #    res = []

    #    for d in self.dogs.all():
    #        t = self.start
    #        while t < self.end:
    #            t += datetime.timedelta(days=7)
                
            

        

class ScheduleEntry(TimeStampedModel):
    class Meta:
        ordering = ('pk',)
        
    start = models.DateTimeField(verbose_name="Start")
    end = models.DateTimeField(verbose_name="End")
    walker = models.ForeignKey(Walker)
    node = models.ForeignKey(Node)
    schedule = models.ForeignKey(Schedule, related_name='entries')
    action = models.CharField(max_length = 200, null=True, blank=True)

