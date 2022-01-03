import math
import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission

from app import settings
from app.utils import response, paginate
from notifications.models import Notifications
from .models import Customer as CustomerModel
from .serializer import CustomerLoginSerializer, CustomerSerializer
from .service import CustomerService


class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        response = Response()
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            # print(User.objects.all())
            user_obj = User.objects.filter(username=username).first()
            status_customer = user_obj.staff.status
            if user_obj is None:
                raise AuthenticationFailed('User not found!')

            customer_obj = CustomerModel.objects.filter(user=user_obj).first()
            if not customer_obj.is_verified:
                return Response('customer is not verified check your mail.')

            user = authenticate(username=username, password=password)
            print(user)
            if user is None:
                raise AuthenticationFailed('Incorrect password!')
            if status_customer is False:
                raise AuthenticationFailed('Staff is inactive!')
            login(request, user)
            cus_serializer = CustomerLoginSerializer(data={
                'username': customer_obj.user.username,
                'password': customer_obj.user.password
                }
            )
            cus_serializer.is_valid(raise_exception=True)
            roles = ''
            for g in customer_obj.user.groups.all():
                roles += g.name + ' '
            token, created = Token.objects.get_or_create(user=user_obj)
            response.data = {
                'token': token.key,
                'user': {
                    'id': customer_obj.id,
                    'username': customer_obj.user.username,
                    'email': customer_obj.user.email,
                    'address': customer_obj.address,
                    'phone_number': customer_obj.phone_number,
                    'full_name': customer_obj.user.last_name + ' ' + customer_obj.user.first_name,
                    'rolesName': roles
                }
            }
        return response


class RegisterView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        global serializer
        username = request.data.get('username')
        email = request.data['email']
        password = request.data['password']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        address = request.data['address']
        phone_number = request.data['phone_number']
        try:
            if User.objects.filter(customer__deleted_at=False, username=username).first():
                return Response('Username is taken.')

            if User.objects.filter(customer__deleted_at=False, email=email).first():
                return Response('Email is taken.')
            auth_token = str(uuid.uuid4())
            serializer = CustomerSerializer(data={
                'user': {
                    'email': email,
                    'username': username,
                    'password': password,
                    'last_name': last_name,
                    'first_name': first_name
                },
                'address': address,
                'phone_number': phone_number,
                'auth_token': auth_token,
            }
            )
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                serializer.save()
            send_mail_after_registration(email, auth_token)
            # notification
            try:
                user = User.objects.get(id=request.user.id)
                obj_notification = Notifications()
                obj_notification.created_by = user
                obj_notification.notification = "Customer " + username + " have been created"
                obj_notification.save()
            except:
                print("An exception occurred")
            # end notification
        except Exception as e:
            print(e)
        content = response(serializer.data, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)


class Verify(APIView):
    def get(self, request, auth_token):
        try:
            customer_obj = CustomerModel.objects.filter(auth_token=auth_token).first()

            if customer_obj:
                if customer_obj.is_verified:
                    content = response('Your account has been verified.', 'successfully', True)
                    return Response(data=content, status=status.HTTP_200_OK)
                customer_obj.is_verified = True
                customer_obj.save()
                content = response('Your account has been verified.', 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            else:
                content = response('error', 'successfully', True)
                return Response(data=content, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print(e)
            content = response('error', 'successfully', True)
            return Response(data=content, status=status.HTTP_406_NOT_ACCEPTABLE)


# class Reset(APIView):
#     def get(self, request, pk):
#         try:
#             send_mail_reset_password(request.data['email'], pk)
#         except Exception as e:
#             print(e)
#             content = response('error', 'successfully', True)
#             return Response(data=content, status=status.HTTP_406_NOT_ACCEPTABLE)

# def send_mail_reset_password(email, pk):
#     subject = 'Reset Password'
#     message = f'Hi paste the link to reset your account http://localhost:8080/reset-password/{pk}'
#     recipient_list = [email]
#     send_mail(subject=subject, from_email=settings.EMAIL_HOST_USER,
#               recipient_list=recipient_list,
#               message=message,
#               fail_silently=True)

def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/api/v1/verify/{token}'
    recipient_list = [email]
    print("aaaaa")
    send_mail(subject=subject, from_email=settings.EMAIL_HOST_USER,
              recipient_list=recipient_list,
              message=message,
              fail_silently=True)


class LogoutView(APIView):
    authentication_classes = (BasicAuthentication)

    def post(self, request):
        logout(request)
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


@api_view(['GET'])
# @login_required(login_url='/example url you want redirect/')
def get_list_no_paginate(request):
    user_service = CustomerService()
    user = request.user
    # print(request.headers)
    # print(available_perm_status(request.user))
    if True:
        colors = user_service.get_list_no_paginate()
        content = response(colors, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


class CustomerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = CustomerService()

    def get(self, request):
        user = request.user
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        if has_permission(user, 'view_customer'):
            [users, count] = self.user_service.index()
            content = response(users[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_customer'):
            if User.objects.filter(customer__deleted_at=False, username=request.data['username']).first():
                return Response('Username is taken.')
            if User.objects.filter(customer__deleted_at=False, email=request.data['email']).first():
                return Response('Email is taken.')
            user = self.user_service.store(request)
            content = response(user, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        pk = request.query_params["id"]
        if has_permission(request.user, 'change_customer') or request.user.id == User.objects.get(customer=pk).id:
            user = self.user_service.update(request, pk)
            if user is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(user, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_customer'):
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
    user_service = CustomerService()
    user = request.user
    if has_permission(user, 'view_customer') or request.user.id == User.objects.get(customer=pk).id:
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
@csrf_protect
def activate(request, pk):
    user_service = CustomerService()
    user = request.user
    if has_permission(user, 'change_customer') or request.user.id == User.objects.get(customer=pk).id:
        user = user_service.activate(pk)
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




@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request, pk):
    user_service = CustomerService()
    user = request.user
    if has_permission(user, 'change_customer') or request.user.id == User.objects.get(customer=pk).id:
        user = user_service.change_password(request, pk)
        if user is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response('change password successfully', 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)