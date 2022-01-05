from django.contrib.auth.models import User

from chats.models import ChatRoom
from chats.serializer import ChatRoomSerializer


class ChatRoomRepository:
    def __init__(self):
        pass

    def active(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = ChatRoomSerializer(objUpdate)
        return serializer.data

    def get_list_no_paginate(self):

        chat_rooms = ChatRoom.objects.filter(deleted_at=False).order_by('-id')
        data = []
        for room in chat_rooms:
            print(room.users.all())
            data.append({
                'id': room.id,
                'name': room.name,
                'created_at': room.created_at,
                'updated_at': room.updated_at,
                'status': room.status,
                'users': room.users.all().values('id', 'username', 'email'),
            })
        # serializer = ChatRoomSerializer(data=list(chat_rooms), many=True)
        # serializer.is_valid(raise_exception=True)
        return data

    def index(self):
        chat_rooms = ChatRoom.objects.filter(deleted_at=False).order_by('-id')
        data = []
        for room in chat_rooms:
            # print(room.users.all())
            data.append({
                'id': room.id,
                'name': room.name,
                'created_at': room.created_at,
                'updated_at': room.updated_at,
                'status': room.status,
                'users': room.users.all().values('id', 'username', 'email'),
            })
        return [data, len(data)]

    def store(self, request):
        context = {'request': request}
        serializer = ChatRoomSerializer(data={
            'name': request.data['name'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update(self, objUpdate, request):
        objUpdate.name = request.data['name']
        objUpdate.status = request.data['status']
        users = User.objects.filter(id__in=request.data['user_id'])
        print(objUpdate.users.clear())
        print(users)
        for user in users:
            objUpdate.users.add(user)
        user_admin = User.objects.filter(groups__name='admin')
        for admin in user_admin:
            objUpdate.users.add(admin)
        objUpdate.save()
        serializer = ChatRoomSerializer(objUpdate)
        return serializer.data

    def show(self, pk):
        chat_room = ChatRoom.objects.get(deleted_at=False, id=pk)
        list_id = []
        for ids in chat_room.users.all().values('id'):
            list_id.append(ids['id'])
        # print(list_id)
        data = ({
            'id': chat_room.id,
            'name': chat_room.name,
            'status': chat_room.status,
            'created_at': chat_room.created_at,
            'updated_at': chat_room.updated_at,
            'user_id': list_id,
        })
        # serializer = ChatRoomSerializer(data, many=False)
        return data

    def destroy(self, pk):
        objDestroy = ChatRoom.objects.get(id=pk)
        objDestroy.delete()
        serializer = ChatRoomSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        return serializer.data
