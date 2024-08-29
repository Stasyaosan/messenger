from django.urls import path
from . import cunsumers

websocket_urlpatterns = {
    path('ws/chat/<str:room_name>/', cunsumers.ChatConsumers.as_asgi())
}
