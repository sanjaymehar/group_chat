import json
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatGroup, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group_id = await self.get_group_id()
        self.user = self.scope['user']
        # self.is_member = await self.check_membership()
        # if not self.is_member:
        #     await self.close()
        # else:
        await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("disconnected",close_code)

    @database_sync_to_async
    def get_group_id(self):
        try:
            group = ChatGroup.objects.get(name=self.group_name)
            return group.id
        except ObjectDoesNotExist:
            print("group not found")
            return None

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        #await self.save_message(message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def check_membership(self):
        try:
            group = ChatGroup.objects.get(name=self.group_name)
            return group.users.filter(id=self.user.id).exists()
        except ObjectDoesNotExist:
            return False

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=message)

    @database_sync_to_async
    def save_message(self, message):
        Message.objects.create(user=self.user, group_id=self.group_id, content=message)
