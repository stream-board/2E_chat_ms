from django.views.generic import TemplateView
from django.views.generic import View

from django.http import JsonResponse

from django.shortcuts import render

from .models import ChatRoom
from .models import ChatMessage

def index(request):

    # Render that in the index template
    return render(request, "index.html")


class ChatRoomView(View):
    def get(self, request, *args, **kwargs):
        chat_messages = ChatMessage.objects.filter(
            chat_room_id=kwargs['room_id'],
        );

        return JsonResponse({
            'status': 200,
            'room_id': kwargs['room_id'],
            'chat_messages': [{
                'sender': chat_message.sender,
                'message': chat_message.message
            } for chat_message in chat_messages]
        })
