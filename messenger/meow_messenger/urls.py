from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('ajaxReg', ajaxReg),
    path('ajaxAuth', ajaxAuth),
    path('suc/<str:token>', suc_user),
    path('profile', profile),
    path('logout', logout),
    # path('settings', settings),
    path('create_chat', create_chat),
    path('chat/<int:id>', get_chat),
    path('add_user/<int:id_chat>/<int:id_user>', add_user),
    path('settings_chat', settings_chat),
    path('del_chat/<int:id_chat>', del_chat),
    path('del_mess/<int:id_message>/<int:id_chat>', delete_message)
]
