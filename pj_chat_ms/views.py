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

        return JsonResponse({
            'status': 200,
            'room_id': kwargs['room_id'],
            'chat_messages': [{
                'sender': chat_message.sender,
                'message': chat_message.message
            } for chat_message in chat_messages]
        })


class ChatRoomCreateView(View):
    def post(self, request, *args, **kwargs):
        chat_room_id = request.POST['id']
        status = 400
        message = 'Bad request'

        if chat_room_id:
            chat_room = ChatRoom(id=chat_room_id)
            chat_room.save()
            status = 200
            message = 'Room created'

        return JsonResponse({
            'status': status,
            'message': message
        })


class ChatRoomDeleteView(View):
    def delete(self, request, *args, **kwargs):
        chat_room= get_object_or_404(ChatRoom, chat_room_id=kwargs['room_id'])
        chat_room.delete()

        return JsonResponse({
            'status': 200,
            'message': 'Room deleted'
        })
