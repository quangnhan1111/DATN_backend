from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rolepermissions.roles import assign_role, clear_roles

from app.roles import Staff as StaffRole, Admin
from customers.serializer import UserSerializer
from .models import Staff


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    write_only_fields = 'password'

    class Meta:
        model = Staff
        fields = "__all__"

    def create(self, validated_data):
        listRole = self.context['request'].data['roles'].split(",")
        user_data = validated_data.pop('user', None)
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        staff = Staff.objects.create(user=user, **validated_data)
        Group.objects.all()
        staff.user.groups.clear()
        clear_roles(staff.user)
        print(listRole)
        for role in listRole:
            if role == 'admin':
                assign_role(staff.user, Admin)
            if role == 'staff':
                assign_role(staff.user, StaffRole)
        return staff

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.email = user_data.get('email', user.email)
        user.username = user_data.get('username', user.username)
        user.last_name = user_data.get('last_name', user.last_name)
        user.first_name = user_data.get('first_name', user.first_name)
        # if user_data.get('password'):
        #     user.set_password(user_data.get('password'))
        user.save()
        listRole = self.context['request'].data['roles'].split(",")
        user.groups.clear()
        clear_roles(user)
        for role in listRole:
            if role == 'admin':
                assign_role(user, Admin)
            if role == 'staff':
                assign_role(user, StaffRole)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    write_only_fields = 'password'
