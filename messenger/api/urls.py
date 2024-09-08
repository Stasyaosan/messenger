from django.urls import path
from .views import *

urlpatterns = [
    path('get_messages/<int:id_chat>/<int:count>', get_messages),
    path('get_chats', get_chats),
    path('add_chat', add_chat),
    path('del_chat', del_chat),
    path('auth', auth)
]
