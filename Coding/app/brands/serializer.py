from rest_framework import serializers

from brands.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        # fields = "__all__"
        fields = ('id', 'name', 'created_at', 'updated_at', 'status')

    def validate_name(self, value):
        if not value.isalnum():
            raise serializers.ValidationError('Name Brand must have not special character.')
        return value

    def create(self, validated_data):
        brand = Brand.objects.create(**validated_data)
        brand.save()
        return brand

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
