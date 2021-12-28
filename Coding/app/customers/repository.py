import uuid

from django.contrib.auth.models import User
from django.db.models import F, Value
from django.db.models.functions import Concat

from customers.models import Customer as CustomerModel
from customers.serializer import CustomerSerializer
from notifications.models import Notifications


class UserRepository:
    def __init__(self):
        pass

    def change_password(self, request, objUpdate):
        objUpdate.set_password(request.data['password'])
        objUpdate.save()
        return objUpdate

    def activate(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = CustomerSerializer(objUpdate)
        return serializer.data

    def get_list_no_paginate(self):
        customers = CustomerModel.objects.filter(deleted_at=False).order_by('-id') \
            .annotate(username=F('user__username'),
                      email=F('user__email'),
                      full_name=Concat('user__first_name', Value(' '), 'user__last_name')
                      ) \
            .values('id', 'address', 'phone_number', 'is_verified',
                    'created_at', 'updated_at', 'email',
                    'username', 'full_name', 'status')
        # serializer = CustomerSerializer(data=list(customers), many=True)
        # serializer.is_valid(raise_exception=True)
        return customers

    def index(self):
        customers = CustomerModel.objects.filter(deleted_at=False).order_by('-id') \
            .annotate(username=F('user__username'),
                      email=F('user__email'),
                      full_name=Concat('user__first_name', Value(' '), 'user__last_name')
                      ) \
            .values('id', 'address', 'phone_number', 'is_verified',
                    'created_at', 'updated_at', 'email',
                    'username', 'full_name', 'status')
        # serializer = CustomerSerializer(data=list(customers), many=True)
        # serializer.is_valid(raise_exception=True)
        return [customers, customers.count()]

    def store(self, request):
        context = {'request': request}
        auth_token = str(uuid.uuid4())
        serializer = CustomerSerializer(data={
            'user': {
                'email': request.data['email'],
                'username': request.data['username'],
                'password': request.data['password'],
                'last_name': request.data['last_name'],
                'first_name': request.data['first_name']
            },
            'address': request.data['address'],
            'phone_number': request.data['phone_number'],
            'auth_token': auth_token,
            'is_verified': True,
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Customer " + request.data['username'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):

        context = {'request': request}
        old_name = objUpdate.user.username
        print("asds")
        serializer = CustomerSerializer(instance=objUpdate, data={
            'user': {
                'email': request.data['email'],
                'username': request.data['username'],
                'password': request.data.get('password', 'None'),
                'last_name': request.data['last_name'],
                'first_name': request.data['first_name']
            },
            'address': request.data['address'],
            'phone_number': request.data['phone_number'],
            'auth_token': request.data.get('auth_token', 'None'),
            'status': request.data['status'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Customer " + old_name + " have been updated "
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def show(self, pk):
        user = CustomerModel.objects.filter(deleted_at=False, id=pk).get()
        serializer = CustomerSerializer(user, many=False)
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = CustomerModel.objects.get(id=pk)
        objDestroy.delete()
        serializer = CustomerSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Customer " + objDestroy.user.username + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data
