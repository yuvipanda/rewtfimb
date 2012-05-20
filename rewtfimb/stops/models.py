from django.contrib.gis.db import models

class Stop(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(null=True, blank=True)
    city = models.ForeignKey('cities.City')

    objects = models.GeoManager()
