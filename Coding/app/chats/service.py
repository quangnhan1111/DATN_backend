from chats.models import ChatRoom
from chats.repository import ChatRoomRepository


class ChatRoomService:
    def __init__(self):
        self.chat_room_repository = ChatRoomRepository()


    def active(self, pk):
        if ChatRoom.objects.filter(deleted_at=False, id=pk).exists():
            objUpdate = ChatRoom.objects.get(pk=pk)
            chat_room = self.chat_room_repository.active(objUpdate)
            return chat_room
        return None

    def get_list_no_paginate(self):
        chat_rooms = self.chat_room_repository.get_list_no_paginate()
        return chat_rooms

    def index(self):
        chat_rooms = self.chat_room_repository.index()
        return chat_rooms

    def store(self, request):
        data = self.chat_room_repository.store(request)
        return data

    def show(self, pk):
        if ChatRoom.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if ChatRoom.objects.filter(deleted_at=False, id=pk).exists():
            return self.chat_room_repository.show(pk)
        return None

    def update(self, request, pk):
        if ChatRoom.objects.filter(deleted_at=False, id=pk).exists():
            objUpdate = ChatRoom.objects.get(pk=pk)
            chat_room = self.chat_room_repository.update(objUpdate, request)
            return chat_room
        return None

    def destroy(self, pk):
        if ChatRoom.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if ChatRoom.objects.filter(deleted_at=False, id=pk).exists():
            return self.chat_room_repository.destroy(pk)
        return None





