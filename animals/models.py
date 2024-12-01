from django.db import models

# Create your models here.
from django.utils import timezone
import json

class Animal(models.Model):
    ANIMAL_CHOICES = [
        ('mouton', 'Mouton'),
        ('chat', 'Chat'),
        ('chien', 'Chien'),
    ]
    
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.CharField(max_length=50, choices=ANIMAL_CHOICES,default='mouton')  # Utilisation de choices
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='animal_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class GPSData(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='gps_data')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    raw_data = models.TextField()

    def __str__(self):
        return f"GPS data for {self.animal.name} at {self.timestamp}"

    def save(self, *args, **kwargs):
        # Sérialiser les données GPS en JSON pour stocker dans raw_data
        self.raw_data = json.dumps({
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat()
        })
        super(GPSData, self).save(*args, **kwargs)
