# Generated by Django 5.1.1 on 2024-10-11 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chatsession_user1_alter_chatsession_user2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chat',
        ),
    ]