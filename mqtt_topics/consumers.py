import json
import os
import django
from mqttasgi.consumers import MqttConsumer
import ssl
import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetGPS.settings')
django.setup()

# Informations du broker MQTT
MQTT_BROKER = "io.adafruit.com"
MQTT_PORT = 8883   # Port WebSocket sécurisé
MQTT_USERNAME = "oueslati_amira"
MQTT_KEY = "aio_vild18GhRIWF3YqMpHrfKlyf82FQ"
TOPICS = [
    "oueslati_amira/feeds/mouton1",
    "oueslati_amira/feeds/mouton2",
    "oueslati_amira/feeds/mouton3"
]

class AnimalTrackingConsumer(MqttConsumer):
    async def connect(self):
        """
        Se connecter au broker MQTT via WebSocket sécurisé (port 443) et s'abonner aux topics.
        """
        print("Connexion au broker MQTT via WebSocket sécurisé...")
        try:
            # Spécifier le protocole SSL pour la connexion sécurisée
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.set_ciphers('TLS_AES_128_GCM_SHA256')  # Optionnel : définir les suites de chiffrement si nécessaire.
            
            # Connexion avec les informations du broker
            self.client = await self.connect_mqtt(
                host=MQTT_BROKER,
                port=8883,  # Utilisation du port sécurisé pour MQTT (8883)
                username=MQTT_USERNAME,
                password=MQTT_KEY,
                ssl_context=self.ssl_context
            )

            # Abonnement aux topics
            for topic in TOPICS:
                await self.subscribe(topic, qos=2)
                print(f"Abonné avec succès au topic : {topic}")

            # Attendre un peu pour garantir que la connexion et les abonnements sont pris en compte
            await asyncio.sleep(2)

        except Exception as e:
            print(f"Erreur lors de la connexion ou de l'abonnement aux topics : {e}")
            logging.error(f"Erreur lors de la connexion ou de l'abonnement aux topics : {e}")


    async def receive(self, data, topic):
        """
        Traiter les messages reçus depuis MQTT.
        """
        print(f"--- Début de la fonction receive ---")
        print(f"Topic reçu : {topic}")
        print(f"Données brutes reçues : {data}")

        try:
            # Vérification si les données sont non vides
            if not data:
                print("Aucune donnée reçue.")
                return

            print("Tentative de parsing des données JSON...")
            # Analyse des données au format JSON
            message = json.loads(data)
            print("Parsing JSON réussi.")

            # Extraction des données
            animal_id = message.get('ID', 'Inconnu')
            latitude = message.get('Lat', 'Inconnu')
            longitude = message.get('Lng', 'Inconnu')

            print(f"Données extraites :")
            print(f"  ID de l'animal : {animal_id}")
            print(f"  Latitude : {latitude}")
            print(f"  Longitude : {longitude}")

            # Logique supplémentaire ici (ex. sauvegarde ou envoi via WebSocket)
            await self.send_json({
                "animal_id": animal_id,
                "latitude": latitude,
                "longitude": longitude
            })

        except json.JSONDecodeError as e:
            print(f"Erreur de parsing JSON : {e}")
        except Exception as e:
            print(f"Erreur inattendue dans la fonction receive : {e}")
        finally:
            print(f"--- Fin de la fonction receive ---")

    async def animal_update(self, event):
        """
        Diffuser les mises à jour via WebSocket.
        """
        try:
            message = event["message"]
            print(f"Diffusion WebSocket : {message}")
            # Envoi du message à tous les clients connectés via WebSocket
            await self.send_json({
                "update": message
            })
        except Exception as e:
            print(f"Erreur lors de la diffusion WebSocket : {e}")
