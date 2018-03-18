from django.contrib import admin

from django.urls import path

from .views import index
from .views import ChatRoomView
from .views import RoomCreateView
from .views import RoomDeleteView

urlpatterns = [
    path('', index, name='index'),
    path('chat/<int:room_id>/', ChatRoomView.as_view(), name='chat'),
    path('room/', RoomCreateView.as_view(), name='create_room'),
    path('room/<int:room_id>/', RoomDeleteView.as_view(), name='delete_room'),
    path('admin/', admin.site.urls),

]
