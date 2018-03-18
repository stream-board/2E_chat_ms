from django.db import models

class ChatRoom(models.Model):
    chat_room_id = models.PositiveIntegerField(
        primary_key=True
    )


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(
        'pj_chat_ms.ChatRoom',
        on_delete=models.CASCADE,
        verbose_name='chat room',
    )

    sender = models.CharField(
        max_length=128,
        verbose_name='sender',
    )

    message = models.CharField(
        max_length=128,
        verbose_name='message',
    )
