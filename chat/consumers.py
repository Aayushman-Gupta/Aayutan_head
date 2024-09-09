from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
import json


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get chat box id
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        # TODO : Check whether chat_id is valid or not and store it in self.chat
        self.chat = None

        # Group name limit is just 100 characters
        self.group_name = "chat_%s" % self.chat_id
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Accept connection
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Received Data
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Store message in DB
        Message.objects.create(
            chat=self.chat,
            
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )
    # Receive message from room group.

    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]
        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )

    pass
