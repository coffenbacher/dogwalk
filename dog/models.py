from django_extensions.db.models import TimeStampedModel
from django.db import models
from bitfield import BitField
from route.models import Node

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
    node = models.ForeignKey(Node, blank=True, related_name='dogs')

    def save(self, *args, **kwargs):
        if self.address:
            n = Node(address=self.address)
            n.save() 
            self.node_id = n.id
        return super(Dog, self).save()

    def __unicode__(self):
        return self.name
        
class RequiredWalk(TimeStampedModel):
    dog = models.ForeignKey(Dog)
    after = models.TimeField(verbose_name="Pick up after", null=True, blank=True)
    before = models.TimeField(verbose_name="Drop off before", null=True, blank=True)
    days = BitField(flags = DAYS)

    def __unicode__(self):
        return 'Required walk for %s' % self.dog

class Walker(TimeStampedModel):
    name = models.CharField(max_length=200)
    address = models.TextField()
    node = models.ForeignKey(Node, related_name='walkers')

    def save(self, *args, **kwargs):
        if self.address:
            n = Node(address=self.address)
            n.save() 
            self.node_id = n.id
        return super(Dog, self).save()

    def __unicode__(self):
        return self.name

class WalkingLocation(TimeStampedModel):
    address = models.TextField()
    node = models.ForeignKey(Node)
    
    def save(self, *args, **kwargs):
        if self.address:
            n = Node(address=self.address)
            n.save() 
            self.node_id = n.id
        return super(Dog, self).save()
    
    def __unicode__(self):
        return self.address
    
