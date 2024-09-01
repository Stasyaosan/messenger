import base64

import django
from django.core.files.base import ContentFile

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
                img = ''
                print(message.file)
                if message.file != '':
                    if str(message.file).endswith('wav'):
                        img = '<audio id="audioPlayback" controls="" style="display: block;" src="media/' + str(
                            message.file) + '"></audio>'
                    else:
                        img = f'<img src="/media/{message.file}" width="100px">'
                rr = ''

                res_date = ''
                date_d = str(message.datetime).split()[0].split('-')
                date_t = str(message.datetime).split()[1].split('.')[0].split(':')
                res_date += f'{date_d[2]}.{date_d[1]}.{date_d[0]}'
                res_date += f' {int(date_t[0]) + 3}:{date_t[1]}'
                if message.user.email == d['user']:
                    rr += f'<a class="btn btn-danger" href="/del_mess/{message.id}/{d['chat']}">Удалить</a>'
                    res += "<div class='message'><div class='user'>" + message.user.login + "</div><span class='text'><p>" + img + "</p>" + message.text + "<br /><span style='font-size: 11px'>" + res_date + "</span>" + rr + "</span></div>"
                else:
                    res += "<div class='message'><div class='user'>" + message.user.login + "</div><span class='text'><p>" + img + "</p>" + message.text + "<br /><span style='font-size: 11px'>" + res_date + "</span>" + rr + "</span></div>"
            return res

        else:
            m = Message()
            m.text = d['message']
            m.chat = Group_chat.objects.filter(id=d['chat']).first()
            m.user = User.objects.filter(email=d['user']).first()
            if 'file' in d:
                print(d)
                file_data = d['file'].split(';base64,')[1]
                file_content = base64.b64decode(file_data)
                m.file.save(d['filename'], ContentFile(file_content))

            m.save()

            messager = Message.objects.filter(chat=Group_chat.objects.filter(id=d['chat']).first())
            res = ''
            for message in messager:
                img = ''
                print(message.file)
                if message.file != '':
                    if str(message.file).endswith('wav'):
                        img = '<audio id="audioPlayback" controls="" style="display: block;" src="media/' + str(
                            message.file) + '"></audio>'
                    else:
                        img = f'<img src="/media/{message.file}" width="100px">'
                rr = ''

                res_date = ''
                date_d = str(message.datetime).split()[0].split('-')
                date_t = str(message.datetime).split()[1].split('.')[0].split(':')
                res_date += f'{date_d[2]}.{date_d[1]}.{date_d[0]}'
                res_date += f' {int(date_t[0]) + 3}:{date_t[1]}'
                if message.user.email == d['user']:
                    rr += f'<a class="btn btn-danger" href="/del_mess/{message.id}/{d['chat']}">Удалить</a>'
                    res += "<div class='message'><div class='user'>" + message.user.login + "</div><span class='text'><p>" + img + "</p>" + message.text + "<br /><span style='font-size: 11px'>" + res_date + "</span>" + rr + "</span></div>"
                else:
                    res += "<div class='message'><div class='user'>" + message.user.login + "</div><span class='text'><p>" + img + "</p>" + message.text + "<br /><span style='font-size: 11px'>" + res_date + "</span>" + rr + "</span></div>"
            return res

            return ""

    async def websocket_receive(self, text_data):
        response = await self.save_message(json.loads(text_data['text']))
        await self.send(text_data=json.dumps({"message": response}))

    async def disconnect(self, close_code):
        pass
