from django.db import models

# Create your models here.
class NodeLocation(models.Model):
    address = models.TextField()

class DistanceEdge(models.Model):
    locations = models.ManyToManyField(NodeLocation)
    miles = models.FloatField()
    minutes = models.FloatField()
