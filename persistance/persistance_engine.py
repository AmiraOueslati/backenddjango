
import pyrebase
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import importlib

# Configuration Firebase
firebase_config = {
    "apiKey": "AIzaSyA3aQXfod9RvXnHePujDz00Atty3y5NE9M",
    "authDomain": "djangoproject-5c131.firebaseapp.com",
    "databaseURL": "https://djangoproject-5c131-default-rtdb.firebaseio.com",
    "projectId": "djangoproject-5c131",
    "storageBucket": "djangoproject-5c131.appspot.com",
    "messagingSenderId": "180286697544",
    "appId": "1:180286697544:web:7a9f443eeab84edef8e87d"
}

# Initialisation de Firebase Realtime Database
firebase = pyrebase.initialize_app(firebase_config)
database = firebase.database()

# Initialisation de Firestore
cred = credentials.Certificate(r"C:\key_private.json")  # Chemin vers votre clé privée Firebase
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()


def persist_data(animal_name, latitude, longitude):
    """
    Sauvegarde les données GPS dans Firebase Realtime Database et Firestore.
    """
    try:
        # Préparer les données
        data = {
            'animal': animal_name,
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': datetime.now().isoformat()  # Timestamp au format ISO 8601
        }

        # Sauvegarder dans Firebase Realtime Database
        database.child('gps_tracking').push(data)

        # Sauvegarder dans Firebase Firestore
        doc_ref = db_firestore.collection("gps_tracking").document()
        doc_ref.set(data)

        print("Données GPS sauvegardées avec succès dans Firebase.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")

import importlib
from datetime import datetime

async def persist_animal(animal_data):
    try:
        # Importation dynamique du module models
        models = importlib.import_module("animals.models")
        print("Persist animal called")
        
        # Affichage des modèles pour vérifier l'importation
        print(models)
        print(models.Animal)
        
        # Extraction des données reçues depuis Django
        animal_id = animal_data.get("id")
        latitude = animal_data.get("latitude")
        longitude = animal_data.get("longitude")
        start_time = animal_data.get("start_time", datetime.now())  # Date par défaut si non fournie
        
        # Affichage des données extraites
        print(f"Received data: id={animal_id}, latitude={latitude}, longitude={longitude}, start_time={start_time}")

        # Recherche de l'animal existant par ID
        animal = await models.Animal.objects.aget(id=animal_id)  # Utilisation de 'aget' pour récupérer l'animal par ID
        
        # Mise à jour des informations GPS de l'animal
        animal.latitude = latitude
        animal.longitude = longitude
        animal.start_time = start_time  # Vous pouvez mettre à jour la date si nécessaire
        
        # Sauvegarde des modifications
        await animal.asave()
        
        print(f"Animal updated: {animal}")
        
    except models.Animal.DoesNotExist:
        # Si l'animal n'existe pas, créez un nouveau
        print(f"Animal with id {animal_id} does not exist, creating a new one...")
        animal = await models.Animal.objects.acreate(
            id=animal_id,
            latitude=latitude,
            longitude=longitude,
            start_time=start_time
        )
        print(f"New animal created: {animal}")
        
    except KeyError as e:
        # Gestion des erreurs liées aux clés manquantes dans 'animal_data'
        print(f"Missing key in animal data: {e}")
        
    except Exception as e:
        # Capturer d'autres erreurs non anticipées
        print(f"Error: {e}")