import json

from django.views.generic import View

from django.http import JsonResponse

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import ChatRoom
from .models import ChatMessage


#test
def index(request):

    # Render that in the index template
    return render(request, "index.html")


class ChatRoomView(View):
    def get(self, request, *args, **kwargs):
        print(request);
        chat_room = get_object_or_404(ChatRoom, id=kwargs['room_id'])
        chat_messages = ChatMessage.objects.filter(
            chat_room=chat_room,
        )

        return JsonResponse([{
            'id': chat_message.id,
            'user_id': chat_message.user_id,
            'message': chat_message.message
        } for chat_message in chat_messages],
            safe=False
        )

    def delete(self, request, *args, **kwargs):
        chat_room = get_object_or_404(ChatRoom, id=kwargs['room_id'])
        chat_room.delete()

        return JsonResponse({
            'id': kwargs['room_id']
        })


class ChatRoomCreateView(View):
    def post(self, request, *args, **kwargs):
        chat_room_obj = json.loads(request.body)
        chat_room = None

        if (
            chat_room_obj['id'] and
            not ChatRoom.objects.filter(id=chat_room_obj['id']).exists()
        ):
            chat_room = ChatRoom(id=chat_room_obj['id'])
            chat_room.save()

        return JsonResponse({
            'id': chat_room.id if chat_room else 'Room exits'
        })
