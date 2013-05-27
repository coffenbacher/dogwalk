from dateutil import parser
from dogwalk.logformats import MSLogEntry
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
        ('Monday'),
        ('Tuesday'),
        ('Wednesday'),
        ('Thursday'),
        ('Friday'),
        ('Saturday'),
        ('Sunday'),
        )

ABSOLUTELY_NOT = 10**5
REQUIRED = -10**6

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
            self.start = parser.parse(self.start + ' EST')
        
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
    pwalker = models.ForeignKey('PWalker', related_name='events')
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
        #TODO
        return self.pdogs.filter(carried=False)
            
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
        return not self.carrying.count() and not self.solution.available().count()
    
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
        if not self.carrying.all().count():
            self.drive_home()
        elif self.all_dogs_want_to_walk():
            self.play()
        elif self.carrying.all().count():
            self.drop_closest()
        self.log('confused')    
        self.wait(minutes=10)

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
        if self.full(walked=0) or self.all_dogs_want_to_walk() or self.last_trip():
            self.play()
        elif not self.all_dogs_want_to_walk():
            self.drop_closest()
        else:
            self.end_day()

    def drop_or_pick(self):    
        self.log('drop or pick?')
        pdogs = list(self.carrying.all()) + list(self.solution.available().all()) 
        
        best = sorted(pdogs, key=lambda n: n.score(self))
        
        for b in best:
            rw = b.get_required_walk(self.time)
            if b.pwalker == self and (rw and b.walked >= rw.count or not rw and b.walked):
                self.drop(b)
                break
            elif b.score(self) > 0:
                self.log('nothing desirable')
                self.end_day()
                break
            elif not b.walked:
                self.pick(b)
                break
        
    def drop_closest(self):
        pdogs = self.carrying.filter(walked__gt=0)
        self.log('drop closest')
        
        best = sorted(pdogs, key=lambda n: n.score(self))[0]
        self.drop(best)
        
    def drop(self, pdog):
        self.log('drop %s' % pdog)
        self.node = pdog.node
        self.carrying.remove(pdog)
        self.save(action='Drop off')

        pdog.dropped_off(self)
    
    def pick(self, pdog):
        self.log('pick %s' % pdog)
        self.node = pdog.node
        self.carrying.add(pdog)
        self.save(action='Pick up')
        
        pdog.picked_up(self)
    
    def play(self):
        self.log('play')
        if not self.all_dogs_want_to_walk():
            self.log('already walked at least all but 1 dogs')
            self.drop_closest()
        
        self.node = self.get_play_location().node
        if PWalker.objects.exclude(pk=self.pk).filter(node = self.node):
            self.wait(minutes=10) 
        else:
            [pdog.play() for pdog in self.carrying.all()]
            self.save()
        
    def get_play_location(self):
        return self.solution.schedule.walkinglocations.all()[0]
    
    def full(self, *args, **kwargs):
        return self.carrying.filter(**kwargs).count() == self.capacity

    def all_dogs_want_to_walk(self):
        for pd in self.carrying.filter(walked__gte = 1):
            rw = pd.dog.requiredwalks.filter(date = self.time.date())
            if not rw or pd.walked > rw[0].count:
                return False
        return True

    def last_trip(self):
        return self.carrying.filter(walked=0).count() and not self.solution.available().count()

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
    walked = models.PositiveIntegerField(default=0)
    carried = models.BooleanField(default=False)

    def get_desirable_times(self):
        return [(rw.after, rw.before) for rw in self.dog.requiredwalks.all()]
    
    def play(self): #fix this for multiple days
        self.walked += 1
        self.events.create(time = self.pwalker.time, pwalker = self.pwalker, type='Walk')
        self.save()

    def picked_up(self, pwalker):
        self.carried = True
        self.pwalker = pwalker
        self.save()
        self.events.create(time = self.pwalker.time, pwalker = self.pwalker, type='Picked up')

    def dropped_off(self, pwalker):
        self.events.create(time = pwalker.time, pwalker = pwalker, type='Dropped off')
        self.pwalker = None
        self.carried = False
        self.save()

    def get_required_walk(self, time):
        rw = self.dog.requiredwalks.filter(date = time.date())
        
        if not rw:
            rw = self.dog.requiredwalks.filter(days = RequiredWalk.days.__getattr__(DAYS[time.weekday()]))
        
        if rw:
            return rw[0]

    def during_a_required_time(self, time):
        rw = self.get_required_walk(time)
        any_rw = self.dog.requiredwalks.exists() # BUG specific date required walks will break this. should only be for generic days
        
        # If required walks are set for this dog then we need to respect them
        if any_rw:
           # If there is a required walk today we need to respect it. Otherwise we're not walking today.
           if rw:
               if rw.after and rw.before:
                   if time.time() >= rw.after and time.time() <= rw.before:
                       return REQUIRED #required to walk during this time
                   else:
                       return ABSOLUTELY_NOT + 14
               if rw.after:
                   if time.time() >= rw.after:
                       return REQUIRED
                   else:
                       return ABSOLUTELY_NOT + 15
               if rw.before:
                   if time.time() <= rw.before:
                       return REQUIRED
                   else:
                       return ABSOLUTELY_NOT + 16
               return REQUIRED
           else:
               return ABSOLUTELY_NOT + 17
        return 0        

    def walked_during_last_day(self, time):
        if self.get_walked_times(time__gte = time - datetime.timedelta(hours = 16)):
            return ABSOLUTELY_NOT # too many walks last day
        return 0        

    def walked_too_many_times_during_last_week(self, time):    
        if self.get_walked_times(time__gt = time - datetime.timedelta(days = 7, hours = -8)).count() >= self.dog.days:
            return ABSOLUTELY_NOT # too many walks this week
        return 0    
    
    def weight_based_on_spacing(self, time):
        if self.dog.days <= 3 and self.get_walked_times(time__gte = time - datetime.timedelta(hours = 40)):
            return ABSOLUTELY_NOT
        return 0    

    def weight_based_on_multiple_walks(self, time):
        rw = self.get_required_walk(time)
        if rw and self.walked < rw.count:
            return ABSOLUTELY_NOT
        return 0    
    
    def weight_based_on_until(self, time):
        for rw in self.dog.requiredwalks.all():
            if rw.date == time.date() and time.time() < rw.until:
                return ABSOLUTELY_NOT
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

    def get_same_walker(self, pwalker):
        s = 0
        if self.events.filter(type='Walk').exclude(pwalker=pwalker):
            return ABSOLUTELY_NOT
        else:
            return 100

    def get_time_desirability(self, time):
        s = {}
        s['required'] = self.during_a_required_time(time)
        s['during_last_day'] = self.walked_during_last_day(time)
        s['too_many'] = self.walked_too_many_times_during_last_week(time)
        s['weight_days'] = self.weight_based_on_days()
        s['spacing'] = self.weight_based_on_spacing(time)
        s['until'] = self.weight_based_on_until(time)
        s['multiple'] = self.weight_based_on_multiple_walks(time)
        s['cancelled'] = self.cancelled(time)
        return s

    def get_walked_times(self, **kwargs):
        return self.events.filter(type='Walk').filter(**kwargs)
    
    def cancelled(self, time):
        if self.dog.cancellations.filter(
            date__gte = time.date() + datetime.timedelta(days = -5.0 / self.dog.days + 1),
            date__lte = time.date() + datetime.timedelta(days = 5.0 / self.dog.days - 1)
            ):
            return 9999
        return 0    
        
    def score(self, pwalker):
        score = {}
        score['distance'] = self.node.get_distance(pwalker.node)
        score['being_walked'] = self.being_walked()
        score['incompatible_dogs'] = self.incompatible_dogs(pwalker.carrying.all())
        score['time'] = self.get_time_desirability(pwalker.time)
        score['same_walker'] = self.get_same_walker(pwalker)
        s = sum((score['distance'], score['being_walked'], score['incompatible_dogs'], sum(score['time'].values()), score['same_walker']))
        
        ms_logger.debug(MSLogEntry(pwalker, self, s, score))
        
        return s

    def next_date(self):
        self.walked = 0
        self.save()
    
    def validate(self):
        events = self.get_walked_times()
        s = self.solution.schedule.start
        w = self.solution.schedule.end
        walked_events = events.filter(time__gte = s, time__lte = w) # fix for multiple weeks
        cancellations = self.dog.cancellations.filter(date__gte = s, date__lte = w)
        
        res = (walked_events.count() + cancellations.count() == self.dog.days)
        

        if self.dog.requiredwalks.exists():
            all_week_events = self.events.filter(time__gte = s, time__lte = w)
            res = res and all([self.__validate_required(all_week_events, rw) for rw in self.dog.requiredwalks.all()])
        
        d = {
            'start'         : s,
            'end'           : w,
            'dog'           : self.dog,
            'days'          : self.dog.days,
            'events'        : walked_events.count(),
            'cancellations' : cancellations.count(),
        }
        mv_logger.debug(str(res), extra=d)
        
        return res
    
    def __validate_required(self, events, rw):
        for e in events:
            print self.dog.name, e.time.time()
            if rw.after and e.time.time() <= rw.after:
                print "f"
                return False
            if rw.before and e.time.time() >= rw.before:
                print "f"
                return False
            if rw.days and not rw.days.__getattr__(DAYS[e.time.weekday()]):
                print "f"
                return False
        return True        
            


    def __repr__(self):
        return self.dog.name.strip()
    
    def __unicode__(self):
        return self.dog.name.strip()
