from django.db import models
from health_app.models import Patient
class ChatSession(models.Model):
    chat_id = models.CharField(max_length=64, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(Patient, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Patient, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    seen =models.BooleanField(default=False)
    