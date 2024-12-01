from datetime import datetime
from mqtt_topics.models import LocationData

class SQLiteClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def insert_location(self, animal_id, latitude, longitude, timestamp, battery=0, speed=0, is_inside_geofence=True):
        """
        Insert a new location record into the SQLite database
        """
        LocationData.objects.create(
            animal_id=animal_id,
            latitude=latitude,
            longitude=longitude,
            battery=battery,
            speed=speed,
            is_inside_geofence=is_inside_geofence
        )

    def get_locations(self, animal_id, start_date=None, end_date=None):
        """
        Get location history for a specific animal
        """
        query = LocationData.objects.filter(animal_id=animal_id)
        
        if start_date:
            query = query.filter(timestamp__gte=start_date)
        if end_date:
            query = query.filter(timestamp__lte=end_date)
            
        return query.order_by('-timestamp')

    def get_latest_location(self, animal_id):
        """
        Get the most recent location for a specific animal
        """
        try:
            return LocationData.objects.filter(animal_id=animal_id).latest('timestamp')
        except LocationData.DoesNotExist:
            return None
