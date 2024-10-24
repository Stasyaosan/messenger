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
    path('get_users', get_users),
    path('add_user_to_chat', add_user_to_chat),
    path('delete_user_to_chat', delete_user_to_chat),
    path('get_users_from_chat', get_users_from_chat),
]
