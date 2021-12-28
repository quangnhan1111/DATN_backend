from django.contrib import admin

from .models import ChatRoom, ChatMessage

admin.site.register(ChatMessage)
admin.site.register(ChatRoom)
