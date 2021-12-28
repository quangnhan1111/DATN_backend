from django.urls import path

from . import views
from .views import ChatRoomView

urlpatterns = [

    path('chat', views.messages_page, name='chat'),
    path('room', views.room, name='room'),
    path('history/<int:id_room>', views.history, name='history'),

    path('chat-room-activate/<int:pk>', views.activate, name='brand-activation'),
    path('chat-room-list-no-page', views.get_list_no_paginate_chat_room, name='chat-room-list-no-page'),
    path('chat-room/<int:pk>', views.get_details_chat_room),
    path('chat-rooms', ChatRoomView.as_view()),
]
