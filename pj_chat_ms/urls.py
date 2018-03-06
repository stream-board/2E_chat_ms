from django.contrib import admin

from django.urls import path

from .views import index
from .views import ChatRoomView

urlpatterns = [
    path('', index, name='index'),
    path('chat/<int:room_id>/', ChatRoomView.as_view(), name='chat'),
    path('admin/', admin.site.urls),

]
