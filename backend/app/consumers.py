import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    GROUP_NAME = 'chat_group'

    async def connect(self):
        await self.channel_layer.group_add(
            self.GROUP_NAME,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.GROUP_NAME,
            self.channel_name
        )

    async def broadcast_message(self, event):
        message = event['message']
        await self.send_message(message)

    async def send_message(self, message):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',  # NOTE: This is for the frontend
            'message': message,
        }))
