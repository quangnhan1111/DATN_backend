from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

    # def validate_name(self, value):
    #     if not value.isalnum():
    #         raise serializers.ValidationError('Name Brand must have not special character.')
    #     return value

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        review.save()
        return review

    def update(self, instance, validated_data):
        instance.star = validated_data.get('star', instance.star)
        instance.content = validated_data.get('content', instance.content)
        instance.product = validated_data.get('product', instance.product)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()
        return instance
