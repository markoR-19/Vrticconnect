from channels.generic.websocket import AsyncWebsocketConsumer
import json
from unidecode import unidecode
from channels.db import database_sync_to_async
from .models import Poruka, Grupa
from django.utils import timezone

class grupaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.grupa = self.scope['url_route']['kwargs']['grupa']
        self.grupa_naziv = 'chat_%s' % str(unidecode(self.grupa))
        
        await self.channel_layer.group_add(
            self.grupa_naziv,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.grupa_naziv,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        grupa_poruke = await database_sync_to_async(Grupa.objects.get)(Naziv=self.grupa)

        poruka = Poruka(
            Tekst_poruka=message,
            Autor=self.scope['user'],
            Grupa=grupa_poruke,
            Datum_objave=timezone.now()
            )

        await database_sync_to_async(poruka.save)()

        await self.channel_layer.group_send(
            self.grupa_naziv,
            {
                'type':'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
                        
        await self.send(text_data=json.dumps({
            'message':message,
            'username': username,
        }))
