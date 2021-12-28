from rest_framework import serializers

from categories.models import Category
from subcategories.models import SubCategory
from subcategories.serializer import SubCategorySerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        if not value.isalnum():
            raise serializers.ValidationError('Name Category must have not special character.')
        return value

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    children = SubCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'children']
