from django.contrib.auth.models import User
from rest_framework import serializers

from chats.models import ChatRoom, ChatMessage


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('id', 'name', 'created_at', 'updated_at', 'status')

    def create(self, validated_data):
        chat_room = ChatRoom.objects.create(**validated_data)
        chat_room.save()
        request = self.context['request']
        print(request.data['user_id'])
        users = User.objects.filter(id__in=request.data['user_id'])
        print(users)
        for user in users:
            chat_room.users.add(user)
        #     add admin vao all group
        user_admin = User.objects.filter(groups__name='admin')
        for admin in user_admin:
            chat_room.users.add(admin)
        return chat_room


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'chat_room', 'username', 'message', 'created_at', 'updated_at')
