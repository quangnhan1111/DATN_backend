from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image_name = validated_data.get('image_name', instance.image_name)
        instance.image_link = validated_data.get('image_link', instance.image_link)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
