import math

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import Staff
from .serializer import StaffLoginSerializer
from .service import StaffService
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission, has_role

from app.utils import response, paginate


class LoginProfileView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        response = Response()
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')

            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                raise AuthenticationFailed('User not found!')

            profile_obj = Staff.objects.filter(user=user_obj).first()
            if profile_obj is None:
                raise AuthenticationFailed('User not found!')
            print(password)
            user = authenticate(username=username, password=password)
            if user is None:
                raise AuthenticationFailed('Incorrect password!')

            login(request, user)
            serializer = StaffLoginSerializer(data={
                'username': profile_obj.user.username,
                'password': profile_obj.user.password
            }
            )
            serializer.is_valid(raise_exception=True)
            roles = []
            for g in profile_obj.user.groups.all():
                roles.append(g.name)
            token, created = Token.objects.get_or_create(user=user_obj)
            response.data = {
                'token': token.key,
                'info': {
                    'id': profile_obj.id,
                    'username': profile_obj.user.username,
                    'address': profile_obj.address,
                    'phone_number': profile_obj.phone_number,
                    'full_name': profile_obj.user.last_name + ' ' + profile_obj.user.first_name,
                    'rolesName': roles
                }
            }
        return response


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_list_admin_and_staff(request):
    user_service = StaffService()
    user = request.user
    print(user)
    if has_permission(user, 'view_staff'):
        users = user_service.get_list_admin_and_staff()
        content = response(users, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = StaffService()

    def get(self, request):
        # print(available_perm_status(request.user))
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        if has_permission(request.user, 'view_staff'):
            [users, count] = self.user_service.index()
            content = response(users[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        # print(request.user)
        listRole = request.data['roles'].split(",")
        if has_permission(request.user, 'add_staff'):
            if User.objects.filter(staff__deleted_at=False, username=request.data['username']).first():
                return Response('Username is taken.')

            if User.objects.filter(staff__deleted_at=False, email=request.data['email']).first():
                return Response('Email is taken.')
            if request.user.groups.filter(name='admin').exists():
                for role in listRole:
                    if role == 'admin':
                        return Response('ko the luu role admin')
                user = self.user_service.store(request)
                content = response(user, 'successfully', True)
                return Response(data=content, status=status.HTTP_201_CREATED)
            for role in listRole:
                if role == 'admin' or role == 'staff':
                    return Response('ko the luu role admin hay staff')
            user = self.user_service.store(request)
            content = response(user, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        pk = request.query_params["id"]
        userUpdate = Staff.objects.get(pk=pk)
        # print(request.user.groups.all())
        listRole = request.data['roles'].split(",")
        if has_permission(request.user, 'change_staff') or request.user.id == User.objects.get(staff=pk).id:
            # print(request.user.groups.values()[0])
            print(userUpdate.user.groups.all())
            if request.user.groups.values()[0]['name'] == userUpdate.user.groups.values()[0]['name']:
                user = self.user_service.update(request, pk)
                if user is None:
                    content = response(None, 'None Object', True)
                    return Response(data=content, status=status.HTTP_204_NO_CONTENT)
                content = response(user, 'successfully', True)
                return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
            if request.user.groups.filter(name='admin').exists():
                for role in listRole:
                    if role == 'admin':
                        return Response('ko the luu role admin')
                if userUpdate.user.groups.filter(name='admin').exists():
                    return Response('ko the update role admin khac')
                user = self.user_service.update(request, pk)
                if user is None:
                    content = response(None, 'None Object', True)
                    return Response(data=content, status=status.HTTP_204_NO_CONTENT)
                content = response(user, 'successfully', True)
                return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
                # serializer = ProfileSerializer(user, many=False)
                # return Response(serializer.data)
            for role in listRole:
                if role == 'admin' or role == 'staff':
                    return Response('ko the luu role admin hay staff')
            user = self.user_service.update(request, pk)
            if user is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(user, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        pk = request.query_params["id"]
        userDestroy = Staff.objects.get(id=pk)
        if has_permission(request.user, 'delete_staff'):
            if has_role(request.user, 'admin'):
                if userDestroy.user.groups.filter(name='admin').exists():
                    return Response('ko the delete role admin khac')
                user = self.user_service.destroy(request, pk)
                if user is None:
                    content = response(None, 'None Object', True)
                    return Response(data=content, status=status.HTTP_204_NO_CONTENT)
                if user == 'obj destroyed':
                    content = response(None, 'Object Destroyed', True)
                    return Response(data=content, status=status.HTTP_204_NO_CONTENT)
                content = response(user, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)

        if has_role(request.user, 'staff'):
            if userDestroy.user.groups.filter(name__in=['admin', 'staff']).exists():
                return Response('ko the delete admin hay staff')
            user = self.user_service.destroy(request, pk)
            if user is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if user == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(user, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_details(request, pk):
    user_service = StaffService()
    # print(available_perm_status(request.user))
    if has_permission(request.user, 'view_staff') or request.user.id == User.objects.get(staff=pk).id:
        if has_role(request.user, 'admin'):
            user = user_service.show(pk)
            if user is None:
                content = response('NONE', 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            content = response(user, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)

        userTarget = User.objects.get(staff=pk)
        if has_role(userTarget, 'admin'):
            return Response('User cant find User with role is Admin')
        user = user_service.show(pk)
        if user is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if user == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(user, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activate(request, pk):
    user_service = StaffService()
    # print(available_perm_status(request.user))
    if has_permission(request.user, 'change_staff') or request.user.id == User.objects.get(staff=pk).id:
        if has_role(request.user, 'admin'):
            user = user_service.activate(pk)
            if user is None:
                content = response('NONE', 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            content = response(user, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)

        userTarget = User.objects.get(staff=pk)
        if has_role(userTarget, 'admin'):
            return Response('User cant find User with role is Admin')
        user = user_service.activate(pk)
        if user is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(user, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request, pk):
    user_service = StaffService()
    # print(available_perm_status(request.user))
    if has_permission(request.user, 'change_staff') or request.user.id == User.objects.get(staff=pk).id:
        if has_role(request.user, 'admin'):
            user = user_service.change_password(request, pk)
            if user is None:
                content = response('NONE', 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            content = response('change password successfully', 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)

        userTarget = User.objects.get(staff=pk)
        if has_role(userTarget, 'admin'):
            return Response('User cant find User with role is Admin')
        user = user_service.change_password(request, pk)
        if user is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response('change password successfully', 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)
