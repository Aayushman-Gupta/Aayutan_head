from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import Message, ChatSession
from health_app.models import Patient


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get chat box id
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        # TODO : Check whether chat_id is valid or not and store it in self.chat
        self.chat = await sync_to_async(ChatSession.objects.get)(chat_id=self.chat_id)

        # Group name limit is just 100 characters
        self.group_name = 'chat_%s' % self.chat_id
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Accept connection
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Received Data
        message = text_data_json['message']
        sender_username = text_data_json['sender_username']
        receiver_username = text_data_json['receiver_username']

        sender = await sync_to_async(Patient.objects.get)(username=sender_username)
        receiver = await sync_to_async(Patient.objects.get)(username=receiver_username)

        # Store message in DB asynchronously
        await sync_to_async(Message.objects.create)(chat=self.chat, sender=sender, receiver=receiver, body=message)

        # Send message to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chatbox_message',
                'message': message,
                'sender_username': sender_username,
                'receiver_username': receiver_username
            },
        )


    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event['message']
        sender_username = event['sender_username']
        receiver_username = event['receiver_username']

        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'sender_username': sender_username,
                    'receiver_username': receiver_username
                }
            )
        )
    pass
