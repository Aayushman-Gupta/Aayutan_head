from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import Message, ChatSession
from health_app.models import Patient


class ChatRoomConsumer(AsyncWebsocketConsumer):

    socket_connections={}

    async def connect(self):
        self.username =self.scope['url_route']['kwargs']['sender_username']

        # Save socket
        ChatRoomConsumer.socket_connections[self.username]=self.channel_name

        # Accept connection
        await self.accept()


    async def disconnect(self, close_code):
        del ChatRoomConsumer.socket_connections[self.username]


    # This function receive messages from WebSocket.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Received Data
        message = text_data_json['message']
        receiver_username = text_data_json['receiver_username']

        sender = await sync_to_async(Patient.objects.get)(username=self.username)
        receiver = await sync_to_async(Patient.objects.get)(username=receiver_username)

        # Store message in DB asynchronously
        await sync_to_async(Message.objects.create)(sender=sender, receiver=receiver, body=message)


        # Fetch receiver channel_name
        if receiver_username in ChatRoomConsumer.socket_connections:
            receiver_channel_name=ChatRoomConsumer.socket_connections[receiver_username]
            # Send message to group
            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'chatbox.message',
                    'message': message,
                    'sender_username':self.username,
                },
            )


    # Receive message from room group.
    async def chatbox_message(self, event):
        message = event['message']
        sender_username = event['sender_username']

        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                    'message': message,
                    'sender_username': sender_username,
                }
            )
        )
    pass
