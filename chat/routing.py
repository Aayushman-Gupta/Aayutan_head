from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<sender_username>\w+)/$",
            consumers.ChatRoomConsumer.as_asgi()),
]
