from django_extensions.db.models import TimeStampedModel
from django.db import models
from bitfield import BitField
from graph.models import Node

DAYS = (
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
    )

# Create your models here.
class Dog(TimeStampedModel):
    name = models.CharField(max_length=200)
    address = models.TextField()
    days = models.PositiveIntegerField(verbose_name = 'Days requested')
    incompatible = models.ManyToManyField('Dog', null=True, blank=True)
    node = models.OneToOneField(Node, blank=True, related_name='dog')

    def save(self, *args, **kwargs):
        if self.address and not self.pk:
            n = Node(address=self.address)
            n.save() 
            self.node_id = n.id
        return super(Dog, self).save()

    def __unicode__(self):
        return self.name
        
class PreferredWalker(TimeStampedModel):
    dog = models.OneToOneField(Dog)
    walker = models.ForeignKey('Walker')

    def __unicode__(self):
        return '%s > %s' % (self.walker, self.dog)

class CancelledWalk(TimeStampedModel):
    dog = models.ForeignKey(Dog, related_name='cancellations')
    date = models.DateField()
    
    def __unicode__(self):
        return '%s on %s' % (self.dog.name, self.date)

class RequiredWalk(TimeStampedModel):
    dog = models.ForeignKey(Dog, related_name='requiredwalks')
    after = models.TimeField(verbose_name="Pick up after", null=True, blank=True)
    before = models.TimeField(verbose_name="Drop off before", null=True, blank=True)
    until = models.TimeField(verbose_name="Drop off after", null=True, blank=True) #20
    date = models.DateField(null=True, blank=True) # #17
    count = models.PositiveIntegerField(verbose_name="How many dates?", default = 1) #18
    days = BitField(flags = DAYS)

    def __unicode__(self):
        return 'Required walk for %s' % self.dog

class Walker(TimeStampedModel):
    name = models.CharField(max_length=200)
    address = models.TextField()
    node = models.ForeignKey(Node, related_name='walkers')
    capacity = models.PositiveIntegerField(default=9)
    start_time = models.TimeField(default='08:00:00')
    end_time = models.TimeField(default='13:00:00')

    def save(self, *args, **kwargs):
        if self.address and not self.pk:
            n = Node(address=self.address)
            n.save() 
            self.node_id = n.id
        return super(Walker, self).save()

    def __unicode__(self):
        return self.name

class WalkingLocation(TimeStampedModel):
    address = models.TextField()
    node = models.ForeignKey(Node)
    
    def save(self, *args, **kwargs):
        if self.address and not self.pk:
            n = Node(address=self.address)
            n.save() 
            self.node_id = n.id
        return super(WalkingLocation, self).save()
    
    def __unicode__(self):
        return self.address
    
