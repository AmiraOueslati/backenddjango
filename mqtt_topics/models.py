# Create your models here.

from django.db import models

class LocationData(models.Model):
    animal_id = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    battery = models.FloatField(default=0)
    speed = models.FloatField(default=0)
    is_inside_geofence = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['animal_id', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.animal_id} - {self.timestamp}"
