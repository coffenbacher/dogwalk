import datetime
import inspect
import logging
from django_extensions.db.models import TimeStampedModel
from dog.models import *
from graph.models import *
from django.db import models
import pdb

ma_logger = logging.getLogger('MA')
ms_logger = logging.getLogger('MS')
mv_logger = logging.getLogger('MV')

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

ABSOLUTELY_NOT = 10000

class Schedule(TimeStampedModel):
    walkers = models.ManyToManyField(Walker)
    dogs = models.ManyToManyField(Dog)
    walkinglocations = models.ManyToManyField(WalkingLocation)
    start = models.DateField()
    end = models.DateField()
    main_solution = models.ForeignKey('Solution', related_name='main_schedule', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super(Schedule, self).save(*args, **kwargs)
        if not self.pk:
            self.init()
    
    def init(self):    
        s = Solution.objects.get_or_create(schedule = self, date = self.start)[0]
        
        if isinstance(self.start, basestring):
            self.start = datetime.datetime.strptime(self.start, '%Y-%m-%d')
        
        for w in self.walkers.all():
            dt = datetime.datetime(self.start.year, 
                                    self.start.month, 
                                    self.start.day, 
                                    w.start_time.hour, 
                                    w.start_time.minute, 
                                    w.start_time.second)
            PWalker.objects.get_or_create(solution = s, node = w.node, walker = w, time=dt)
        for d in self.dogs.all():
            PDog.objects.get_or_create(solution = s, node = d.node, dog = d)
        
        self.main_solution = s
        self.walkinglocations = WalkingLocation.objects.all() #hack
        self.save()

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

    def choose_solution(self):
        self.main_solution = self.solutions.all()[0] # automatically pick first solution
        self.save()

    def entries_by_walker(self):
        res = []
        for w in self.main_solution.pwalkers.all():
            res.append([w, self.main_solution.entries.filter(pwalker = w)])
        return res
    
    def entries_by_day(self):
        entries = self.main_solution.entries.all()
        days = entries.dates('start', 'day')

        res = []
        for d in days:
            res.append([d, self.main_solution.entries.filter(start__day = d.day).order_by('pwalker', 'start')])
            
        return res
    
    def entries_by_dog(self):
        res = []
        for d in self.main_solution.pdogs.all():
            res.append([d, self.main_solution.entries.filter(node=d.node).order_by('start')])
        return res
        
    #def status_by_dog(self):
    #    res = []

    #    for d in self.dogs.all():
    #        t = self.start
    #        while t < self.end:
    #            t += datetime.timedelta(days=7)

class Event(models.Model):
    pdog = models.ForeignKey('PDog', related_name='events')
    type = models.CharField(max_length = 200)
    time = models.DateTimeField()
                
class Solution(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='solutions')
    date = models.DateField() # flexible
    
    def solved(self):
        return self.date > self.schedule.end
    
    def find_desirable(self): # make sure there is some desirable move for someone left
        for pwalker in self.pwalkers.all():
            pdogs = list(pwalker.carrying.all()) + list(self.available().all()) 
            for p in pdogs:
                if p.score(pwalker) < 0:
                    return True
        
        return False # no desirable found
    
    def day_complete(self):
        if self.date.weekday() >= 5:
            return True


        for pwalker in self.pwalkers.all():
            if pwalker.carrying.count() or not pwalker.home(): 
                return False #require walkers to drop dogs and get home

        if self.find_desirable() and not self.walker_overtime():
            return False # if there's something to do and we're still in the day then we're not done 
        
        return True # No carrying, no available

    def walker_overtime(self):
        for p in self.pwalkers.all():
            if p.time.time() < p.walker.end_time:
                return False
        return True        
                
    def next_date(self):
        self.date = self.date + datetime.timedelta(days=1)
        
        for pwalker in self.pwalkers.all():
            pwalker.next_date()

        for pdog in self.pdogs.all():
            pdog.next_date()
            
        self.save()

    def available(self):
        return self.pdogs.filter(walked=False, carried=False)
    
    def unwalked(self):
        return self.pdogs.filter(walked=False)
        
    def walked(self):
        return self.pdogs.filter(walked=True)
            
    def validate_dogs(self):
        """ Returns boolean, [details] """
        for d in self.pdogs.all():
            if not d.validate(): 
                return False
        return True    

class SolutionEntry(models.Model):
    solution = models.ForeignKey('Solution', related_name='entries')
    pwalker = models.ForeignKey('PWalker')
    node = models.ForeignKey('graph.Node')
    action = models.CharField(null = True, blank = True, max_length = 200)
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
    
    def get_log_info(self):
        d = {   
                'walker':   self.walker.name,
                'time':     self.time,
                'node':     self.node.address,
                'carrying':     str(self.carrying.all()) + ' '*100,
            }
        return d
    
    def log(self, a):
        ma_logger.debug(a, extra=self.get_log_info())
        
    def turn(self):
        self.log('taking turn')
        if self.done():
            self.log('done')
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
        self.log('ending day')
        self.go_home()

    def go_home(self):
        self.log('planning home')
        if self.carrying.filter(walked=True).count():
            self.drop_closest()
        elif self.carrying.filter(walked=False).count():
            self.play()
        elif self.home():
            self.wait(minutes=20) 
        else:
            self.drive_home()

    def wait(self, **kwargs):
        self.log('waiting')
        self.time += datetime.timedelta(**kwargs)
        self.save()

    def drive_home(self):
        self.log('drove home')
        self.node = self.walker.node
        self.save()

    def home(self):
        return self.node == self.walker.node

    def drop_or_play(self):
        self.log('drop or play?')
        if self.full(walked=False) or self.last_trip():
            self.play()
        elif self.carrying.filter(walked=True):
            self.drop_closest()
        else:
            self.end_day()

    def drop_or_pick(self):    
        self.log('drop or pick?')
        pdogs = list(self.carrying.all()) + list(self.solution.available().all()) 
        
        best = sorted(pdogs, key=lambda n: n.score(self))[0]
        
        if best.walked:
            self.drop(best)
        elif best.score(self) > 0:
            self.log('nothing desirable')
            self.end_day()
        else:
            self.pick(best)
        
    def drop_closest(self):
        pdogs = self.carrying.filter(walked=True)
        self.log('drop closest')
        
        best = sorted(pdogs, key=lambda n: n.score(self))[0]
        self.drop(best)
        
    def drop(self, pdog):
        self.log('drop %s' % pdog)
        self.node = pdog.node
        self.carrying.remove(pdog)
        self.save(action='Drop off')

        pdog.pwalker = None
        pdog.carried = False
        pdog.save()
    
    def pick(self, pdog):
        self.log('pick %s' % pdog)
        self.node = pdog.node
        self.carrying.add(pdog)
        self.save(action='Pick up')
        
        pdog.carried = True
        pdog.pwalker = self
        pdog.save()
    
    def play(self):
        self.log('play')
        if self.carrying.filter(walked=True):
            self.log('already walked dogs')
            self.drop_closest()
        self.node = self.get_play_location().node
        [pdog.play() for pdog in self.carrying.all()]
        self.save()
        
    def get_play_location(self):
        return self.solution.schedule.walkinglocations.all()[0]
    
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
            action = None
            if 'action' in kwargs:
                action = kwargs.pop('action')    
            if self.last_entry.node != self.node:
                edge = Edge.objects.filter(nodes=self.last_entry.node).get(nodes = self.node)
                self.time = self.time + datetime.timedelta(seconds=edge.seconds)
                self.last_entry = self.solution.entries.create(pwalker = self, node = self.node, 
                                                                start = self.time, action = action) 
                self.time = self.last_entry.end
            super(PWalker, self).save(*args, **kwargs)
        
    
class PDog(models.Model):
    dog = models.ForeignKey('dog.Dog')
    solution = models.ForeignKey('Solution', related_name='pdogs')
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

    def during_a_required_time(self, time):
        for t in self.get_desirable_times():
            if time >= t[0] and time <= t[1]:
                return -100000 #required to walk during this time
        return 0        

    def walked_during_last_day(self, time):
        if self.get_walked_times(time__gte = time - datetime.timedelta(hours = 16)):
            return 10000 # too many walks last day
        return 0        

    def walked_too_many_times_during_last_week(self, time):    
        if self.get_walked_times(time__gte = time - datetime.timedelta(days = 7)).count() >= self.dog.days:
            return 10000 # too many walks this week
        return 0    
    
    def weight_based_on_days(self):
        return self.dog.days / 5.0 * -10000
            
    def incompatible_dogs(self, others):
        incompat = self.dog.incompatible.all()
        for d in others:
            if d.dog in incompat:
                return ABSOLUTELY_NOT
        return 0     
        
    def being_walked(self):
        # factor in double walks
        if not self.walked and self.pwalker:
            return 1000000
        return 0    

    def get_time_desirability(self, time):
        s = 0
        s += self.during_a_required_time(time)
        s += self.walked_during_last_day(time)
        s += self.walked_too_many_times_during_last_week(time)
        s += self.weight_based_on_days()

        return s

    def log(self, a, pwalker, d, w, i, t, s):
        d = {
            'context'       :   inspect.stack()[3][3] + ' '*100,
            'walker'        :   pwalker.walker.name,
            'w_node'        :   pwalker.node,
            'dog'           :   self,
            'd_node'        :   self.node,
            'time'          :   pwalker.time,
            'd'             :   d,
            'w'             :   w,
            'i'             :   i,
            't'             :   t,
            'score'         :   s,
        }
            
        ms_logger.debug(a, extra=d)

    def get_walked_times(self, **kwargs):
        return self.events.filter(type='Walk').filter(**kwargs)
        
    def score(self, pwalker):
        d = self.node.get_distance(pwalker.node)
        w = self.being_walked()
        i = self.incompatible_dogs(pwalker.carrying.all())
        t = self.get_time_desirability(pwalker.time)
        s = d + t + w + i
        self.log(' ', pwalker, d, w, i, t, s)
        return s

    def next_date(self):
        self.walked = False
        self.save()
    
    def validate(self):
        events = self.get_walked_times()
        s = self.solution.schedule.start
        w = s + datetime.timedelta(days=7)
        week_events = events.filter(time__gte = s, time__lte = w) # fix for multiple weeks
        if week_events.count() != self.dog.days:
            res = False
        else:
            res = True
        
        d = {
            'start'         : s,
            'end'           : w,
            'dog'           : self.dog,
            'days'          : self.dog.days,
            'events'        : week_events.count(),
        }
        mv_logger.debug(str(res), extra=d)
        
        #required = self.dog.requiredwalks.all()
        #for r in required: 
        return res
    
    def __repr__(self):
        return self.dog.name.strip()
    
    def __unicode__(self):
        return self.dog.name.strip()
