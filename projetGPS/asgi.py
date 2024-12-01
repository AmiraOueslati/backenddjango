import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from mqtt_topics.consumers import AnimalTrackingConsumer
from mqtt_topics.routing import websocket_urlpatterns
from projetGPS.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projetGPS.settings')

django.setup()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'mqtt': AnimalTrackingConsumer().as_asgi(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})
