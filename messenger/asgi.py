from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from django.core.asgi import get_asgi_application
from django.urls import path

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger.settings')
from meow_messenger.cunsumers import YourConsumer
from meow_messenger.online import Online

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws', YourConsumer.as_asgi()),
            path('online', Online.as_asgi()),
        ])
    )
})
