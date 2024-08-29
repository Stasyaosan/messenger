import os
from channels.auth import AuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import meow_messenger.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddleware(
        URLRouter(
            messenger.routing.webso
        )
    )
})