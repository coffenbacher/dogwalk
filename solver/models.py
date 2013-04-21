import datetime
from django.db import models
from graph.models import *
from dog.models import *

class Problem(models.Model):
    walkers = models.ManyToManyField('dog.Walker')
    dogs = models.ManyToManyField('dog.Dog')
    walkinglocations = models.ManyToManyField('dog.WalkingLocation')
    main_solution = models.OneToOneField('Solution', related_name='main_problem', null=True)
    start_date = models.DateField(default = datetime.datetime(2013, 03, 01)) # permanent
    
    def save(self, *args, **kwargs):
        super(Problem, self).save(*args, **kwargs)

        s = Solution.objects.get_or_create(problem = self, date = self.start_date)[0]
        for w in self.walkers.all():
            dt = datetime.datetime(self.start_date.year, 
                                    self.start_date.month, 
                                    self.start_date.day, 
                                    w.start_time.hour, 
                                    w.start_time.minute, 
                                    w.start_time.second)
            PWalker.objects.get_or_create(solution = s, node = w.node, walker = w, time=dt)
        for d in self.dogs.all():
            PDog.objects.get_or_create(solution = s, node = d.node, dog = d)
        self.main_solution = s

    def solve(self):
        s = self.main_solution
        skip = True
        while not s.solved():
            if not skip: #complete first day
                s.next_date()        
            skip = False
            while not s.day_complete():
                for w in s.pwalkers.all():
                    w.turn()
            
        return s
        

class Solution(models.Model):
    problem = models.ForeignKey(Problem)
    date = models.DateField() # flexible
    
    def solved(self):

        if not self.date > self.problem.start_date + datetime.timedelta(days=6): #do full week
            return False
            
        if self.unwalked().count():
            return False
    
        for pwalker in self.pwalkers.all():
            if pwalker.carrying.count() or pwalker.node != pwalker.walker.node:
                return False

        return True # No carrying, no available
    
    def find_desirable(self): # make sure there is some desirable move for someone left
        for pwalker in self.pwalkers.all():
            pdogs = list(pwalker.carrying.all()) + list(self.available().all()) 
            for p in pdogs:
                if p.score(pwalker) < 0:
                    return True
        
        return False # no desirable found
    
    def day_complete(self):
        print "Unwalked: ", self.unwalked().count()
        print "Available: ", self.available().count()
        print "Walked: ", self.walked().count()

        if self.date.weekday() >= 5:
            return True

        if self.unwalked().count() and self.find_desirable():
            return False

        for pwalker in self.pwalkers.all():
            if pwalker.carrying.count() or not pwalker.home():
                return False

        return True # No carrying, no available

    def next_date(self):
        self.date = self.date + datetime.timedelta(days=1)
        
        for pwalker in self.pwalkers.all():
            pwalker.next_date()

        for pdog in self.dogs.all():
            pdog.next_date()
            
        self.save()

    def available(self):
        return self.dogs.filter(walked=False, carried=False)
    
    def unwalked(self):
        return self.dogs.filter(walked=False)
        
    def walked(self):
        return self.dogs.filter(walked=True)
    
    
class Event(models.Model):
    pdog = models.ForeignKey('PDog', related_name='events')
    type = models.CharField(max_length = 200)
    time = models.DateTimeField()

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
        print "%s taking turn at" % self.walker.name, self.time
        if self.done():
            print "Done"
        elif self.done_with_dogs() or self.time.time() > self.walker.end_time:
            self.end_day()
        elif (self.carrying.count() >= self.capacity) or not self.solution.available().count():
            self.drop_or_play()
        else:    
            self.drop_or_pick()
    
    def done(self):
        return self.done_with_dogs() and self.node == self.walker.node
        
    def done_with_dogs(self):
        return not self.solution.unwalked() and not self.carrying.count()
    
    def start_day(self):
        d = self.time + datetime.timedelta(days=1)
        s = self.walker.start_time
        self.time = datetime.datetime(d.year, d.month, d.day, s.hour, s.minute, s.second)
        self.save()

    def next_date(self):
        if self.home():
            self.start_day()
        else:
            raise Exception("Walker %s didn't make it home" % self.walker.name)

    def end_day(self):
        print "%s ending day" % self.walker.name
        self.go_home()

    def go_home(self):
        print "%s going home" % self.walker.name
        if self.carrying.filter(walked=False).count():
            self.play()
        elif self.carrying.filter(walked=True).count():
            self.drop_closest()
        else:
            self.node = self.walker.node
            self.save()

    def home(self):
        return self.node == self.walker.node

    def drop_or_play(self):
        print "%s drop_or_play" % self.walker.name
        if self.full(walked=False) or self.last_trip():
            self.play()
        elif self.carrying.filter(walked=True):
            self.drop_closest()
        else:
            self.end_day()

    def drop_or_pick(self):    
        print "%s drop_or_pick" % self.walker.name
        pdogs = list(self.carrying.all()) + list(self.solution.available().all()) 
        
        best = sorted(pdogs, key=lambda n: n.score(self))[0]
        
        if best.walked:
            self.drop(best)
        elif best.score(self) > 0:
            self.end_day()
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
        pdog.carried = False
        pdog.save()
    
    def pick(self, pdog):
        print "%s pick" % self.walker.name
        self.node = pdog.node
        self.carrying.add(pdog)
        self.save()
        
        pdog.carried = True
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
        return self.carrying.filter(walked=False).count() and not self.solution.available().count()

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
    solution = models.ForeignKey('Solution', related_name='dogs')
    pwalker = models.ForeignKey('PWalker', related_name='carrying', null=True)
    node = models.ForeignKey('graph.Node')
    walked = models.BooleanField(default=False)
    carried = models.BooleanField(default=False)

    def get_desirable_times(self):
        return [(rw.after, rw.before) for rw in self.dog.requiredwalks.all()]
    
    def play(self): #fix this for multiple days
        self.walked = True
        self.events.create(time = self.pwalker.time, type='Walk')
        self.save()

    def get_time_desirability(self, time):
        for t in self.get_desirable_times():
            if time >= t[0] and time <= t[1]:
                return -10000 #required to walk during this time
        if self.get_walked_times(time__gte = time - datetime.timedelta(hours = 16)):
            return 1000 # too many walks last day
        if self.get_walked_times(time__gte = time - datetime.timedelta(days = 7)).count() > self.dog.days:
            return 10000 # too many walks this week

        return -1000 #decent       

    def get_walked_times(self, **kwargs):
        return self.events.filter(type='Walk').filter(**kwargs)
        
    def score(self, pwalker):
        if not self.walked and self.pwalker:
            return 10000
        d = self.node.get_distance(pwalker.node)
        t = self.get_time_desirability(pwalker.time)
        return d + t

    def next_date(self):
        self.walked = False
        self.save()
