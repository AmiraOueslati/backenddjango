from pymongo import MongoClient
from django.conf import settings

class MongoDBClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.client = MongoClient(
            host=settings.MONGODB_HOST,
            port=settings.MONGODB_PORT
        )
        self.db = self.client[settings.MONGODB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert_location(self, animal_id, latitude, longitude, timestamp, battery=None, speed=None):
        collection = self.get_collection('location_history')
        document = {
            'animal_id': animal_id,
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp,
            'battery': battery,
            'speed': speed
        }
        return collection.insert_one(document)

    def get_animal_locations(self, animal_id, start_date=None, end_date=None):
        collection = self.get_collection('location_history')
        query = {'animal_id': animal_id}
        
        if start_date or end_date:
            query['timestamp'] = {}
            if start_date:
                query['timestamp']['$gte'] = start_date
            if end_date:
                query['timestamp']['$lte'] = end_date
        
        return list(collection.find(query).sort('timestamp', -1))

    def get_latest_location(self, animal_id):
        collection = self.get_collection('location_history')
        return collection.find_one(
            {'animal_id': animal_id},
            sort=[('timestamp', -1)]
        )

    def get_animal_stats(self, animal_id):
        collection = self.get_collection('location_history')
        pipeline = [
            {'$match': {'animal_id': animal_id}},
            {'$group': {
                '_id': '$animal_id',
                'total_distance': {'$sum': '$distance'},
                'avg_speed': {'$avg': '$speed'},
                'min_battery': {'$min': '$battery'},
                'max_battery': {'$max': '$battery'},
                'last_seen': {'$max': '$timestamp'}
            }}
        ]
        result = list(collection.aggregate(pipeline))
        return result[0] if result else None
