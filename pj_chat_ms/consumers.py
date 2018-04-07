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
        user_id = event.get('user_id')
        message = event.get('message', '')
        print(user_id)

        if category == 'NEW-MESSAGE':
            chat_message = ChatMessage.objects.create(
                chat_room_id=room_id,
                user_id=int(user_id),
                message=message,
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
                        'user_id': user_id,
                        'id': chat_message.id,
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
                        'user_id': user_id,
                    },
                )

    def chat_message(self, event):
        room_id = event.get('room_id')
        user_id = event.get('user_id')
        message = event.get('message')
        chat_message_id = event.get('id', '')

        self.send_json({
            'category': 'NEW-MESSAGE',
            'id': chat_message_id,
            'room_id': room_id,
            'user_id': user_id,
            'message': message,
        })

    def chat_join(self, event):
        user_id = event.get('user_id')
        self.send_json({
            'category': 'JOIN-ROOM',
            'message': JOIN_MESSAGE.format(
                user=user_id,
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
