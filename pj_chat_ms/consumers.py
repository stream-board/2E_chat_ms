from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

from .models import ChatMessage

GROUP_ROOM_CHAT = 'chat-{id}'
JOIN_MESSAGE = '{user} se ha unido a la sala'

class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        async_to_sync(
            self.channel_layer.group_add)(
                GROUP_ROOM_CHAT.format(
                    id=self.scope['url_route']['kwargs']['room_id']
                ),
                self.channel_name
            )
        async_to_sync(self.accept())

    def receive_json(self, event):
        category = event.get('category')
        room_id = event.get('room_id')
        sender = event.get('sender')
        message = event.get('message', '')

        if category == 'NEW-MESSAGE':
            async_to_sync(
                ChatMessage.objects.create(
                    chat_room_id=room_id,
                    sender=sender,
                    message=message,
                )
            )

            async_to_sync(
                self.channel_layer.group_send)(
                    GROUP_ROOM_CHAT.format(
                        id=event['room_id']
                    ),
                    {
                        'type': 'chat.message',
                        'message': message,
                        'room_id': room_id,
                        'sender': sender,
                    },
                )
        elif category == 'JOIN-ROOM':
            async_to_sync(
                self.channel_layer.group_send)(
                    GROUP_ROOM_CHAT.format(
                        id=event['room_id']
                    ),
                    {
                        'type': 'chat.join',
                        'sender': sender,
                    },
                )

    def chat_message(self, event):
        room_id = event.get('room_id')
        sender = event.get('sender')
        message = event.get('message')

        self.send_json({
            'category': 'NEW-MESSAGE',
            'room_id': room_id,
            'sender': sender,
            'message': message,
        })

    def chat_join(self, event):
        sender = event.get('sender')
        self.send_json({
            'category': 'JOIN-ROOM',
            'message': JOIN_MESSAGE.format(
                user=sender,
            ),
        })

    def disconnect(self, code):
        async_to_sync(
            self.channel_layer.group_discard)(
                GROUP_ROOM_CHAT.format(
                    id=self.scope['url_route']['kwargs']['room_id']
                ),
                self.channel_name
            )