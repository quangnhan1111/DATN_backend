import math

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission

from app.utils import response, paginate
from notifications.models import MessageNotifications
from .models import ChatMessage, ChatRoom
from .pusher import pusher_client
from .serializer import ChatMessageSerializer, ChatRoomSerializer
from .service import ChatRoomService


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def messages_page(request):
    serializer = ChatMessageSerializer(data={
        'chat_room': request.data['chat_room'],
        'username': request.data['username'],
        'message': request.data['message'],
    })
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # data = ChatMessage.objects.all().values('id', 'chat_room', 'username', 'message', 'created_at', 'updated_at')
    # print(list(data))
    # serializer = ChatMessageSerializer(data=data, many=True)
    # serializer.is_valid(raise_exception=True)
    # serializer.save()
    pusher_client.trigger('chat', 'message', serializer.data)
    # notification
    try:
        name_chat_room = ChatRoom.objects.get(id=request.data['chat_room']).name
        obj_notification = MessageNotifications()
        obj_notification.notification = "New Message in room " + name_chat_room + \
                                        " by " + request.data['username']
        obj_notification.save()
    except:
        content = response('ERROR', 'successfully', True)
        return Response(data=content, status=status.HTTP_404_NOT_FOUND)
    # # end notification
    content = response('serializer.data', 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def history(request, id_room):
    data = ChatMessage.objects.filter(chat_room=id_room).values('id', 'chat_room', 'username', 'message',
                                                                'created_at', 'updated_at')
    print(data)
    serializer = ChatMessageSerializer(data=list(data), many=True)
    serializer.is_valid(raise_exception=True)
    # pusher_client.trigger('chat', 'message', list(serializer.data))
    content = response(list(data), 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


#
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def room(request):
    assigned_groups = list(request.user.chatroom_set.values_list('id', flat=True))
    groups_participated = ChatRoom.objects.filter(id__in=assigned_groups, deleted_at=False, status=True)
    temp_participants = []
    data = []
    users = ""
    print(groups_participated)
    for chat_group in groups_participated:
        for participants in chat_group.users.values('id', 'username', 'email'):
            print(participants)
            temp_participants.append({
                'id': participants['id'],
                'username': participants['username'],
                'email': participants['email']
            })
            if participants['username'] == request.user.username:
                users += "you, "
            else:
                users += participants['username'] + ", "
        data.append({
            'groups_participated': {
                'id': chat_group.id,
                'name': chat_group.name,
                # 'description': chat_group.description,
                # 'mute_notifications': chat_group.mute_notifications,
                'temp_participants': temp_participants,
                'users': users,
                'username_of_current_user': request.user.username
            },
        })
        users = ""
        temp_participants = []
    content = response(data, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@csrf_protect
def get_list_no_paginate_chat_room(request):
    chat_room_service = ChatRoomService()
    user = request.user
    if has_permission(user, 'view_chat_room'):
        chat_room = chat_room_service.get_list_no_paginate()
        content = response(chat_room, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


class ChatRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.chat_room_service = ChatRoomService()

    def get(self, request):
        # print(request.user)
        # print(available_perm_status(request.user))
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        user = request.user
        if has_permission(user, 'view_chat_room'):
            [chat_rooms, count] = self.chat_room_service.index()
            content = response(chat_rooms[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_chat_room'):
            if ChatRoom.objects.filter(deleted_at=False, name=request.data['name']).first():
                return Response('name Chat Room is taken.')
            if ChatRoom.objects.filter(deleted_at=True, name=request.data['name']).first():
                objRestore = ChatRoom.objects.get(name=request.data['name'])
                objRestore.restore()
                serializer = ChatRoomSerializer(objRestore)
                content = response(serializer.data, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            chat_room = self.chat_room_service.store(request)
            content = response(chat_room, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_chat_room'):
            chat_room = self.chat_room_service.update(request, pk)
            if chat_room is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(chat_room, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_chat_room'):
            chat_room = self.chat_room_service.destroy(pk)
            if chat_room is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if chat_room == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(chat_room, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_details_chat_room(request, pk):
    chat_room_service = ChatRoomService()
    user = request.user
    if has_permission(user, 'view_chat_room'):
        chat_room = chat_room_service.show(pk)
        if chat_room is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if chat_room == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(chat_room, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activate(request, pk):
    chat_room_service = ChatRoomService()
    user = request.user
    if has_permission(user, 'change_chat_room'):
        chat_room = chat_room_service.active(pk)
        if chat_room is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if chat_room == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(chat_room, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)