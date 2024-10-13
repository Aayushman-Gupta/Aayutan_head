from django.db import models
from health_app.models import Patient


class ChatSession(models.Model):
    chat_id = models.CharField(max_length=64, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    # user1 user2 denotes the users associated with a chat
    user1 = models.ForeignKey(
        Patient, related_name='user1', on_delete=models.CASCADE, null=True)
    user2 = models.ForeignKey(
        Patient, related_name='user2', on_delete=models.CASCADE, null=True)

    # TODO : for group chat store users in form of list

    def __str__(self):
        return f"{self.user1}-{self.user2}"


class Message(models.Model):
    # chat = models.ForeignKey(
    #     ChatSession, related_name='chat_session_messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        Patient, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        Patient, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body
