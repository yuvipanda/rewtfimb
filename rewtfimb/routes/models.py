from django.contrib.gis.db import models

class Route(models.Model):
    name = models.CharField(max_length=1024)

class RouteSegment(models.Model):
    start = models.ForeignKey('stops.Stop', related_name='segments_starting')
    end = models.ForeignKey('stops.Stop', related_name='segments_ending')
    route = models.ForeignKey(Route, related_name="segments")
    stops = models.ManyToManyField('stops.Stop', through='SegmentStop')

class SegmentStop(models.Model):
    stop = models.ForeignKey('stops.Stop')
    segment = models.ForeignKey(RouteSegment)
    sequence = models.IntegerField()
