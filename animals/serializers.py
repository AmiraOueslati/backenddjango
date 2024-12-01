from rest_framework import serializers
from .models import Animal, GPSData

class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'name', 'latitude', 'longitude', 'description', 'start_time', 'end_time', 'image']

class GPSDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSData
        fields = ['id', 'animal', 'latitude', 'longitude', 'timestamp']
