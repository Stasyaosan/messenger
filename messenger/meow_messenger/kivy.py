import django

django.setup()
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


class Kivy(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    @sync_to_async
    def save_message(self, d):
        return 'res'

    async def websocket_receive(self, text_data):
        response = await self.save_message(json.loads(text_data['text']))
        await self.send(text_data=json.dumps({"message": response}))

    async def disconnect(self, close_code):
        pass
