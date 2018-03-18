from django.contrib import admin

from django.urls import path

from .views import index
from .views import ChatRoomView
from .views import ChatRoomCreateView
from .views import ChatRoomDeleteView

urlpatterns = [
    path('', index, name='index'),
    path('chat-room/<int:room_id>/', ChatRoomView.as_view(), name='chat'),
    path('chat-room/', ChatRoomCreateView.as_view(), name='create_chat_room'),
    path('chat-room/<int:room_id>/', ChatRoomDeleteView.as_view(), name='delete_chat_room'),
    path('admin/', admin.site.urls),

]
