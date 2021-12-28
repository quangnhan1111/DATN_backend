from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

    def create(self, validated_data):
        coupon = Coupon.objects.create(**validated_data)
        coupon.save()
        return coupon

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.time = validated_data.get('time', instance.time)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.value = validated_data.get('value', instance.value)
        instance.name_code = validated_data.get('name_code', instance.name_code)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
