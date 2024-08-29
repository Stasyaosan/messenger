import django

django.setup()
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from .models import Message, User, Group_chat
import json
from asgiref.sync import sync_to_async


class YourConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    @sync_to_async
    def save_message(self, d):
        if d['message'] == 'list':
            messager = Message.objects.filter(chat=Group_chat.objects.filter(id=d['chat']).first())
            chat = d['chat']
            res = ''
            for message in messager:
                rr = ''
                if message.user.email == d['user']:
                    rr += f'<a class="btn btn-danger" href="/del_mess/{message.id}/{d['chat']}">Удалить</a>'
                    res += "<div class='message bg-secondary-subtle'><div class='user'>" + message.user.login + "</div><span class='text'>" + message.text + "<br/><span style='font-size: 11px'>" + str(
                        message.datetime) + "</span>" + rr + "</div>"
                else:
                    res += "<div class='message'><div class='user'>" + message.user.login + "</div><span class='text'>" + message.text + "</span><span class='datetime'>" + str(
                        message.datetime) + "</span></div>"
            return res

        else:
            m = Message()
            m.text = d['message']
            m.chat = Group_chat.objects.filter(id=d['chat']).first()
            m.user = User.objects.filter(email=d['user']).first()
            m.save()
            return ""

    async def websocket_receive(self, text_data):
        response = await self.save_message(json.loads(text_data['text']))
        await self.send(text_data=json.dumps({"message": response}))

    async def disconnect(self, close_code):
        pass
