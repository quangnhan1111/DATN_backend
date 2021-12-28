from django.conf.urls import url
from django.urls import path, re_path
from notifications import consumer

websocket_urlpatterns = [
    url(r'ws/notification/', consumer.NotificationConsumer.as_asgi()),
    url(r'ws/message/', consumer.MessageNotificationConsumer.as_asgi()),
    url(r'ws/invoice/', consumer.InvoiceNotificationConsumer.as_asgi()),
]