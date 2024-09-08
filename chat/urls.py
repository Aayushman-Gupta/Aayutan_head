from django.contrib import admin
from . import views
# from .views import chat_box
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("create-chat-session/", views.create_chat_session,
         name="create-chat-session")
]
