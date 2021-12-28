from django.conf.urls import url

from chats import consumer

websocket_urlpatterns = [
    # path(r'ws/profile/', consumers.ProfileConsumer.as_asgi()),
    # path(r'ws/coins/', consumers.CoinsConsumer.as_asgi()),
    url(r'ws/chat/', consumer.ChatConsumer.as_asgi()),
]