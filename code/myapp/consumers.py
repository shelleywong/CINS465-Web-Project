# Reference: 2 (see: CINS465-Shelley-Wong, README.md)
# Reference: 3 (see: CINS465-Shelley-Wong, README.md)
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from datetime import datetime

from .models import Chat_Model
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        current_message = text_data_json['message']
        m = Chat_Model(author=self.scope['user'],
            message=text_data_json['message'], message_html=current_message)
        m.save()
        my_dict = {'author' : m.author.username, 'message' : current_message}

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': json.dumps(my_dict)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = json.loads(event['text'])
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message["message"],
            'username': message["author"],
            'created_on': datetime.now().strftime('%m/%d/%Y %H:%M'),

        }))
