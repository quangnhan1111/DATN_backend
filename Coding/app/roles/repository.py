from django.contrib.auth.models import Group, User

from customers.models import Customer
from customers.serializer import CustomerSerializer
from roles.serializer import RoleSerializer
from staffs.models import Staff
from staffs.serializer import StaffSerializer


class RoleRepository:
    def __init__(self):
        pass


    def get_role_by_user(self, pk):
        # data = User.objects.filter(pk=pk).values('groups__name')
        data = User.objects.get(pk=pk)
        name_group = list()
        for i in data.groups.all():
            name_group.append(i.name)
        return name_group[0]

    def get_users_by_role(self, pk):
        global user
        role_name = Group.objects.get(pk=pk).name
        print(role_name)
        if role_name == 'customer':
            customer = Customer.objects.filter(deleted_at=False, user__groups__name='customer').order_by('-id')
            serializer = CustomerSerializer(customer, many=True)
            print(customer)
        else:
            if role_name == 'admin':
                user = Staff.objects.filter(deleted_at=False, user__groups__name='admin').order_by('-id')
            elif role_name == 'staff':
                user = Staff.objects.filter(deleted_at=False, user__groups__name='staff').order_by('-id')

            serializer = StaffSerializer(user, many=True)
        print(serializer.data)
        return serializer.data

    def index(self):
        roles = Group.objects.all().order_by('-id').values()
        print(roles)
        serializer = RoleSerializer(data=list(roles), many=True)
        serializer.is_valid(raise_exception=True)
        return roles

    def store(self, request):
        context = {'request': request}
        serializer = RoleSerializer(data={
            'name': request.data['name'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        serializer = RoleSerializer(instance=objUpdate, data={
            'name': request.data['name'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def show(self, pk):
        if Group.objects.filter(pk=pk).exists():
            role = Group.objects.get(pk=pk)
        else:
            return None
        serializer = RoleSerializer(role, many=False)
        return serializer.data

    def destroy(self, pk):
        objDestroy = Group.objects.get(id=pk)
        objDestroy.delete()
        serializer = RoleSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        return serializer.data
