from django.conf.urls import url
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

from .consumers import ChatConsumer

application = ProtocolTypeRouter({
    # WebSocket chat handler
    "websocket": SessionMiddlewareStack(
        URLRouter([
            path("chat-room/<int:room_id>", ChatConsumer),
        ]),
    )
})
