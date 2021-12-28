from django.contrib.auth.models import User
from django.db.models import F, Value
from django.db.models.functions import Concat

from notifications.models import Notifications
from .models import Staff
from .serializer import StaffSerializer


class StaffRepository:
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
        serializer = StaffSerializer(objUpdate)
        return serializer.data

    def get_list_admin_and_staff(self):
        staffs = Staff.objects.filter(deleted_at=False)\
            .exclude(user__groups__name='admin')\
            .order_by('-id') \
            .annotate(username=F('user__username'),
                      email=F('user__email'),
                      full_name=Concat('user__first_name', Value(' '), 'user__last_name'),) \
            .values('id', 'address', 'phone_number',
                    'created_at', 'updated_at', 'email',
                    'username', 'full_name',
                    'user_id', 'status').order_by('-id')
        return staffs

    def index(self):
        staffs = Staff.objects.filter(deleted_at=False, user__groups__name='staff') \
            .exclude(user__groups__name='admin') \
            .order_by('id') \
            .annotate(username=F('user__username'),
                      email=F('user__email'),
                      full_name=Concat('user__first_name', Value(' '), 'user__last_name'),) \
            .values('id', 'address', 'phone_number',
                    'created_at', 'updated_at', 'email',
                    'username', 'user_id', 'status',
                    'full_name').order_by('-id')
        return [staffs, staffs.count()]

    def store(self, request):
        # user = saveUser(objUpdate, request)
        context = {'request': request}
        serializer = StaffSerializer(data={
            'user': {
                'email': request.data['email'],
                'username': request.data['username'],
                'password': request.data.get('password', 'None'),
                'last_name': request.data['last_name'],
                'first_name': request.data['first_name']
            },
            'address': request.data['address'],
            'phone_number': request.data['phone_number'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Profile " + request.data['username'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        old_name = objUpdate.user.username
        serializer = StaffSerializer(instance=objUpdate, data={
            'user': {
                'email': request.data['email'],
                'username': request.data['username'],
                'password': request.data.get('password', 'None'),
                'last_name': request.data['last_name'],
                'first_name': request.data['first_name']
            },
            'address': request.data['address'],
            'phone_number': request.data['phone_number'],
            'status': request.data['status']
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Profile " + old_name + " have been updated "
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def show(self, pk):
        user = Staff.objects.filter(deleted_at=False, id=pk).get()
        serializer = StaffSerializer(user, many=False)
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = Staff.objects.get(id=pk)
        objDestroy.delete()
        serializer = StaffSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Profile " + objDestroy.user.username + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

