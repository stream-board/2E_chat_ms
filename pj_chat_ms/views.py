from django.views.generic import CreateView
from django.views.generic import TemplateView
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
        chat_room = get_object_or_404(ChatRoom, id=kwargs['room_id'])
        chat_messages = ChatMessage.objects.filter(
            chat_room=chat_room,
        );

        return JsonResponse([{
                'id': chat_message.id,
                'sender': chat_message.sender,
                'message': chat_message.message
            } for chat_message in chat_messages],
            safe=False
        )


class ChatRoomCreateView(View):
    def post(self, request, *args, **kwargs):
        print(request.POST)
        chat_room_id = request.POST.get('id', 0)

        if chat_room_id:
            chat_room = ChatRoom(id=chat_room_id)
            chat_room.save()

        return JsonResponse({
            'id': chat_room_id
        })


class ChatRoomDeleteView(View):
    def delete(self, request, *args, **kwargs):
        chat_room = get_object_or_404(ChatRoom, chat_room_id=kwargs['room_id'])
        chat_room.delete()

        return JsonResponse({
            'id': kwargs['room_id']
        })
