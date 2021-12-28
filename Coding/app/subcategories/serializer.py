from rest_framework import serializers

from subcategories.models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"

    def validate_name(self, value):
        if not value.isalnum():
            raise serializers.ValidationError('Name Category must have not special character.')
        return value

    def create(self, validated_data):
        category = SubCategory.objects.create(**validated_data)
        category.save()
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.category)
        instance.save()
        return instance

