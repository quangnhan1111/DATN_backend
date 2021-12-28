import math

from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import available_perm_status

from app.utils import response, paginate
from roles.service import RoleService


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_role_by_user(request, pk):
    user = request.user
    role_service = RoleService()
    if has_permission(user, 'view_role'):
        group_name = role_service.get_role_by_user(pk)
        if group_name is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(group_name, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_users_by_role(request, pk):
    user = request.user
    role_service = RoleService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    # print(available_perm_status(request.user))
    if has_permission(user, 'view_role'):
        users = role_service.get_users_by_role(pk)
        count = len(users)
        if users is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(users[start:end], 'successfully', True, count, current_page,
                           math.ceil(count / per_page), per_page)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


class RoleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.role_service = RoleService()

    def get(self, request):
        user = request.user
        print(request.user)
        print(available_perm_status(request.user))
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        if has_permission(user, 'view_role'):
            roles = self.role_service.index()
            count = len(roles)
            content = response(roles[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_role'):
            if Group.objects.filter(name=request.data['name']).first():
                return Response('name Group is taken.')
            role = self.role_service.store(request)
            content = response(role, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_role'):
            role = self.role_service.update(request, pk)
            if role is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(role, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_role'):
            role = self.role_service.destroy(pk)
            if role is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(role, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_details(request, pk):
    role_service = RoleService()
    user = request.user
    if has_permission(user, 'view_role'):
        role = role_service.show(pk)
        if role is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(role, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)
