from django.urls import path
from .views import *

urlpatterns = [
    path('get_messages', get_messages),
    path('get_chats', get_chats),
    path('create_chat', create_chat),
    path('del_chat', del_chat),
    path('auth', auth),
    path('reg', reg),
    path('get_id_user', get_id_user),
    path('add_message', add_message),
    path('delete_message', DeleteMessage),
    path('get_users', get_users)
]
