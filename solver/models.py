import datetime
from django.db import models
from graph.models import *
from dog.models import *

class Problem(models.Model):
    walkers = models.ManyToManyField('dog.Walker')
    dogs = models.ManyToManyField('dog.Dog')
    walkinglocations = models.ManyToManyField('dog.WalkingLocation')
    main_solution = models.OneToOneField('Solution', related_name='main_problem', null=True)
    
    def save(self, *args, **kwargs):
        super(Problem, self).save(*args, **kwargs)
        s = Solution.objects.get_or_create(problem = self)[0]
        for w in self.walkers.all():
            PWalker.objects.get_or_create(solution = s, node = w.node, walker = w, time='2013-03-01 10:00:00')
        for d in self.dogs.all():
            PDog.objects.get_or_create(solution = s, node = d.node, dog = d)
        s.pending = s.pdogs.all()
        self.main_solution = s

    def solve(self):
        s = self.main_solution
        while not s.solved():
            for w in s.pwalkers.all():
                w.turn()
        return s
        

class Solution(models.Model):
    problem = models.ForeignKey(Problem)
    pending = models.ManyToManyField('PDog', related_name='pending_pdogs')
    
    def solved(self):
        print "Pending count: ", self.pending.count()
        print "Walkers: ", self.pwalkers.all()
        
        if not self.pending.count():
            for pwalker in self.pwalkers.all():
                if pwalker.carrying.count() or pwalker.node != pwalker.walker.node:
                    return False
            return True # No carrying, no pending
        return False


class SolutionEntry(models.Model):
    solution = models.ForeignKey('Solution', related_name='entries')
    pwalker = models.ForeignKey('PWalker')
    node = models.ForeignKey('graph.Node')
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not isinstance(self.start, datetime.datetime):
            self.end = datetime.datetime.strptime(self.start, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds = self.node.seconds)
        else:    
            self.end = self.start + datetime.timedelta(seconds = self.node.seconds)
            
        super(SolutionEntry, self).save(*args, **kwargs)


class PWalker(models.Model):
    solution = models.ForeignKey('Solution', related_name='pwalkers')
    walker = models.ForeignKey('dog.Walker')
    capacity = models.PositiveIntegerField(default=9)
    last_entry = models.OneToOneField('SolutionEntry', related_name='last_pwalker', null=True)
    node = models.ForeignKey('graph.Node')
    time = models.DateTimeField()
    
    def turn(self):
        print "%s taking turn" % self.walker.name
        if self.done():
            print "Done"
        elif self.done_with_dogs():
            self.go_home()
        elif (self.carrying.count() >= self.capacity) or not self.solution.pending.count():
            self.drop_or_play()
        else:    
            self.drop_or_pick()
    
    def done(self):
        return self.done_with_dogs() and self.node == self.walker.node
        
    def done_with_dogs(self):
        return not self.solution.pending.count() and not self.carrying.count()
    
    def go_home(self):
        print "%s going home" % self.walker.name
        self.node = self.walker.node
        self.save()

    def drop_or_play(self):
        print "%s drop_or_play" % self.walker.name
        if self.full(walked=False) or self.last_trip():
            self.play()
        else:
            self.drop_closest()

    def drop_or_pick(self):    
        print "%s drop_or_pick" % self.walker.name
        pdogs = list(self.carrying.all()) + list(self.solution.pending.all()) 
        
        best = sorted(pdogs, key=lambda n: n.score(self))[0]
        
        if best.walked:
            self.drop(best)
        else:
            self.pick(best)
        
    def drop_closest(self):
        pdogs = self.carrying.filter(walked=True)
        print "%s drop_closest, %s" % (self.walker.name, pdogs)
        
        best = sorted(pdogs, key=lambda n: n.score(self))[0]
        self.drop(best)
        
    def drop(self, pdog):
        print "%s drop" % self.walker.name
        self.node = pdog.node
        self.carrying.remove(pdog)
        self.save()

        pdog.pwalker = None
        pdog.save()
    
    def pick(self, pdog):
        print "%s pick" % self.walker.name
        self.node = pdog.node
        self.solution.pending.remove(pdog)
        self.carrying.add(pdog)
        self.save()
        
        pdog.pwalker = self
        pdog.save()
    
    def play(self):
        print "%s play" % self.walker.name
        self.node = self.get_play_location().node
        [pdog.play() for pdog in self.carrying.all()]
        self.save()
        
    def get_play_location(self):
        return self.solution.problem.walkinglocations.all()[0]
    
    def full(self, *args, **kwargs):
        return self.carrying.filter(**kwargs).count() == self.capacity

    def last_trip(self):
        return self.carrying.filter(walked=False).count() and not self.solution.pending.count()

    def save(self, *args, **kwargs):
        if not self.pk:    
            super(PWalker, self).save(*args, **kwargs)
            e = self.solution.entries.create(pwalker = self, node = self.node, start = self.time)
            self.last_entry = e
            self.save()
        else:    
            if self.last_entry.node != self.node:
                edge = Edge.objects.filter(nodes=self.last_entry.node).get(nodes = self.node)
                self.time = self.time + datetime.timedelta(seconds=edge.seconds)
                self.last_entry = self.solution.entries.create(pwalker = self, node = self.node, 
                                                                start = self.time)
                self.time = self.last_entry.end
            super(PWalker, self).save(*args, **kwargs)
        
    
class PDog(models.Model):
    dog = models.ForeignKey('dog.Dog')
    solution = models.ForeignKey('Solution', related_name='pdogs')
    pwalker = models.ForeignKey('PWalker', related_name='carrying', null=True)
    node = models.ForeignKey('graph.Node')
    walked = models.BooleanField(default=False)

    def get_desirable_times(self):
        return [(rw.after, rw.before) for rw in self.dog.requiredwalks.all()]
    
    def play(self): #fix this for multiple days
        self.walked = True
        self.save()

    def get_time_desirability(self, time):
        for t in self.get_desirable_times():
            if time >= t[0] and time <= t[1]:
                return -1000
        return 0        

    def score(self, pwalker):
        if not self.walked and self.pwalker:
            return 10000
        d = self.node.get_distance(pwalker.node)
        t = self.get_time_desirability(pwalker.time)
        return d + t

# Create your models here.
