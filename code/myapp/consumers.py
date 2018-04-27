# chat/consumers.py
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# import json


# from django.conf import settings

# from channels.generic.websocket import AsyncJsonWebsocketConsumer

# from .exceptions import ClientError
# from .utils import get_room_or_error

from channels.generic.websocket import AsyncWebsocketConsumer
import json

# from channels.auth import channel_session_user_from_http
# from channels import Group
from datetime import datetime


# from channels import Group
# from channels.sessions import channel_session
# from urllib.parse import parse_qs
# from urllib import parse
# from channels import Group
# from channels.sessions import channel_session

#chatdemo
# from channels import Group
# from channels.sessions import channel_session
from .models import Chat_Model
from django.contrib.auth.models import User
# # import json
# from channels.auth import channel_session_user, channel_session_user_from_http
# from django.utils.html import escape
# from django.core import serializers
# import markdown
# import bleach
# import re
# from django.conf import settings
# from django.urls import reverse
# from channels_presence.models import Room
# from channels_presence.decorators import touch_presence
#
# from django.dispatch import receiver
# from channels_presence.signals import presence_changed
# from channels import Group

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

    # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )

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

    # async def chat_message(self, event):
    #     data = event['message']
    #     chat_queryset = Chat_Model.objects.filter(id__lte=data['last_message_id']).order_by("-created_on")[:10]
    #     chat_message_count = len(chat_queryset)
    #     if chat_message_count > 0:
    #         first_message_id = chat_queryset[len(chat_queryset)-1].id
    #     else:
    #         first_message_id = -1
    #     previous_id = -1
    #     if first_message_id != -1:
    #         try:
    #             previous_id = Chat_Model.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
    #         except IndexError:
    #             previous_id = -1

        # chat_messages = reversed(chat_queryset)
        # cleaned_chat_messages = list()
        # for item in chat_messages:
        #     current_message = item.message_html
        #     cleaned_item = {'author' : item.author.username, 'message' : current_message }
        #     cleaned_chat_messages.append(cleaned_item)
        #
        # my_dict = { 'messages' : cleaned_chat_messages, 'previous_id' : previous_id }
        # message.reply_channel.send({'text': json.dumps(my_dict)})
        # # Send message to WebSocket
        # await self.send(text_data=json.dumps({
        #     (my_dict)
        # }))

    #         data = json.loads(message['text'])
    # chat_queryset = ChatMessage.objects.filter(id__lte=data['last_message_id']).order_by("-created")[:10]
    # chat_message_count = len(chat_queryset)
    # if chat_message_count > 0:
    #     first_message_id = chat_queryset[len(chat_queryset)-1].id
    # else:
    #     first_message_id = -1
    # previous_id = -1
    # if first_message_id != -1:
    #     try:
    #         previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
    #     except IndexError:
    #         previous_id = -1
    #
    # chat_messages = reversed(chat_queryset)
    # cleaned_chat_messages = list()
    # for item in chat_messages:
    #     current_message = item.message_html
    #     cleaned_item = {'user' : item.user.username, 'message' : current_message }
    #     cleaned_chat_messages.append(cleaned_item)
    #
    # my_dict = { 'messages' : cleaned_chat_messages, 'previous_id' : previous_id }
    # message.reply_channel.send({'text': json.dumps(my_dict)})

# chat/consumers.py
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# import json

# This is a synchronous WebSocket consumer that accepts all connections, receives
# messages from its client, & echos those messages back to the same client.
# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#
#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         self.accept()
#
#     def disconnect(self, close_code):
#         #Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))


# @channel_session_user_from_http
# def chat_connect(message):
#     Group("all").add(message.reply_channel)
#     Room.objects.add("all", message.reply_channel.name, message.user)
#     message.reply_channel.send({"accept": True})
#
# @touch_presence
# @channel_session_user
# def chat_receive(message):
#     data = json.loads(message['text'])
#     if not data['message']:
#         return
#     if not message.user.is_authenticated:
#         return
#     current_message = escape(data['message'])
#     urlRegex = re.compile(
#             u'(?isu)(\\b(?:https?://|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)[^\\s()<'
#             u'>\\[\\]]+[^\\s`!()\\[\\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])'
#         )
#
#     processed_urls = list()
#     for obj in urlRegex.finditer(current_message):
#         old_url = obj.group(0)
#         if old_url in processed_urls:
#             continue
#         processed_urls.append(old_url)
#         new_url = old_url
#         if not old_url.startswith(('http://', 'https://')):
#             new_url = 'http://' + new_url
#         new_url = '<a href="' + new_url + '">' + new_url + "</a>"
#         current_message = current_message.replace(old_url, new_url)
#     m = ChatMessage(author=message.user, message=data['message'], message_html=current_message)
#     m.save()
#
#     my_dict = {'author' : m.author.username, 'message' : current_message}
#     Group("all").send({'text': json.dumps(my_dict)})
#
# @channel_session_user
# def chat_disconnect(message):
#     Group("all").discard(message.reply_channel)
#     Room.objects.remove("all", message.reply_channel.name)
#
# @receiver(presence_changed)
# def broadcast_presence(sender, room, **kwargs):
#     # Broadcast the new list of present users to the room.
#     Group(room.channel_name).send({
#         'text': json.dumps({
#             'type': 'presence',
#             'payload': {
#                 'channel_name': room.channel_name,
#                 'members': [user.username for user in room.get_users()],
#                 'lurkers': int(room.get_anonymous_count()),
#             }
#         })
#     })
#
# @channel_session_user_from_http
# def loadhistory_connect(message):
#     message.reply_channel.send({"accept": True})
#
# @channel_session_user
# def loadhistory_receive(message):
#     data = json.loads(message['text'])
#     chat_queryset = Chat_Model.objects.filter(id__lte=data['last_message_id']).order_by("-created")[:10]
#     chat_message_count = len(chat_queryset)
#     if chat_message_count > 0:
#         first_message_id = chat_queryset[len(chat_queryset)-1].id
#     else:
#         first_message_id = -1
#     previous_id = -1
#     if first_message_id != -1:
#         try:
#             previous_id = Chat_Model.objects.filter(pk__lt=first_message_id).order_by("-pk")[:1][0].id
#         except IndexError:
#             previous_id = -1
#
#     chat_messages = reversed(chat_queryset)
#     cleaned_chat_messages = list()
#     for item in chat_messages:
#         current_message = item.message_html
#         cleaned_item = {'author' : item.author.username, 'message' : current_message }
#         cleaned_chat_messages.append(cleaned_item)
#
#     my_dict = { 'messages' : cleaned_chat_messages, 'previous_id' : previous_id }
#     message.reply_channel.send({'text': json.dumps(my_dict)})
#
# @channel_session_user
# def loadhistory_disconnect(message):
#     pass
