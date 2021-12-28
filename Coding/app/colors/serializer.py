from rest_framework import serializers

from colors.models import Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"

    # def validate_name(self, value):
    #     if not value.isalnum():
    #         raise serializers.ValidationError('Name Brand must have not special character.')
    #     return value

    def create(self, validated_data):
        category = Color.objects.create(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
