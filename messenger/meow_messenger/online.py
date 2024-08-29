import django

django.setup()
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, User, Group_chat
import json
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta


class Online(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    @sync_to_async
    def online_users(self, d):
        res = ''
        current_chat = Group_chat.objects.filter(id=d['chat']).first()
        current_date = datetime.now().date().strftime('%Y-%m-%d')
        current_time = datetime.now().time().strftime('%H:%M')
        for u in current_chat.users.all():

            res += f'<div class ="row" ><div>'
            if u.avatar == None:
                res += '<img src = "/static/default.png" width = "70px" >'
            else:
                res += '<img src = "/media/' + str(
                    u.avatar) + '" width = "70px"></div><div> ' + u.login + '</div><div>&nbsp;&nbsp;&nbsp;'
                res += u.update_date.strftime("%Y-%m-%d %h:%M")

            if current_date == u.update_date.strftime("%Y-%m-%d"):
                d = str(u.update_date.strftime("%H:%M")).split(':')
                res_d = str(int(d[0]) + 3) + ':' + d[1]

                if current_time == res_d:
                    res += 'Online'
            else:
                res += 'Offline'
        return res

    async def websocket_receive(self, text_data):
        response = await self.online_users(json.loads(text_data['text']))
        await self.send(text_data=json.dumps({"message": response}))

    async def disconnect(self, close_code):
        pass
