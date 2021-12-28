from django.contrib.auth.models import User
from rest_framework import serializers
from rolepermissions.roles import assign_role

from app.roles import Customer
from customers.models import Customer as CustomerModel


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    last_name = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'last_name', 'first_name']

        write_only_fields = 'password'

    # def validate_password(self, value):
    #     if value.isalnum():
    #         raise serializers.ValidationError('password must have atleast one special character.')
    #     return value


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomerModel
        fields = "__all__"
        # fields = ('username', 'email', 'first_name', 'last_name', 'password')
        # read_only_fields = ('draft', 'read_time')
        # write_only_fields = 'password'
        # exclude = ('updated', 'created',)

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        # print(user_data)
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        customer = CustomerModel.objects.create(user=user, **validated_data)
        assign_role(user, Customer)
        return customer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        user.email = user_data.get('email', user.email)
        user.username = user_data.get('username', user.username)
        user.last_name = user_data.get('last_name', user.last_name)
        user.first_name = user_data.get('first_name', user.first_name)
        # if user_data.get('password') is not None:
        #     user.set_password(user_data.get('password'))
        user.save()
        # assign_role(user, Customer)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.status = validated_data.get('status', instance.status)
        # instance.auth_token = validated_data.get('auth_token', instance.auth_token)
        instance.save()
        return instance

    def validate(self, data):
        # print(data)
        if data['user']['first_name'] == data['user']['last_name']:
            raise serializers.ValidationError("first_name and last_name shouldn't be same.")
        return data

    # def to_internal_value(self, data):
    #     user_data = data['user']
    #     return super().to_internal_value(user_data)

    # def to_internal_value(self, value):
    #     value['date_joined'] = parser.parse(value['date_joined'])
    #     return super().to_internal_value(value)

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance


class CustomerLoginSerializer(serializers.Serializer):
    # username = serializers.CharField(max_length=100)
    # password = serializers.CharField(max_length=100, write_only=True)
    class Meta:
        model = CustomerModel
        fields = ['username', 'password']
        write_only_fields = 'password'
