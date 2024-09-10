from django.contrib import admin
from . import views
# from .views import chat_box
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("create-chat-session/",
         views.create_chat_session,
         name="create_chat_session"),

    path("get-chat-messages/<str:chat_id>/",
         views.get_chat_messages,
         name="get_chat_messages"),

    path('delete-chat-session/<str:chat_id>/',
         views.delete_chat_session,
         name='delete_chat_session'),

    path('delete-message/<str:message_id>/',
         views.delete_message,
         name='delete_message')
]
