from django.contrib.auth.models import Group
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        role = Group.objects.create(**validated_data)
        role.save()
        return role

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
