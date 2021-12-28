from django.contrib.auth.models import User
from django.db.models import F

from notifications.models import Notifications
from .models import Post
from .serializer import PostSerializer


class PostRepository:
    def __init__(self):
        pass

    def activate(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = PostSerializer(objUpdate)
        return serializer.data

    def get_list_no_page(self):
        posts = Post.objects.filter(deleted_at=False).annotate(lastUpdated=F('updated_at')) \
            .values('id', 'title', 'content', 'image_name', 'image_link', 'lastUpdated', 'created_at', 'status') \
            .order_by('-id')

        serializer = PostSerializer(data=list(posts), many=True)
        serializer.is_valid(raise_exception=True)
        return posts

    def index(self):
        posts = Post.objects.filter(deleted_at=False).annotate(lastUpdated=F('updated_at')) \
            .values('id', 'title', 'content', 'image_name', 'image_link', 'lastUpdated', 'created_at', 'status') \
            .order_by('-id')

        serializer = PostSerializer(data=list(posts), many=True)
        serializer.is_valid(raise_exception=True)
        return [posts, posts.count()]

    def show(self, pk):
        posts = Post.objects.filter(id=pk, deleted_at=False).annotate(lastUpdated=F('updated_at')) \
            .values('id', 'title', 'content', 'image_name', 'image_link', 'lastUpdated', 'created_at', 'status') \
            .order_by('id')
        print(posts.query)
        return posts

    def store(self, request):
        context = {'request': request}
        serializer = PostSerializer(data={
            'title': request.data['title'],
            'content': request.data['content'],
            'image_name': request.data['image_name'],
            'image_link': request.data['image_link'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Post " + request.data['title'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        old_name = objUpdate.title
        serializer = PostSerializer(instance=objUpdate, data={
            'title': request.data['title'],
            'content': request.data['content'],
            'image_name': request.data['image_name'],
            'image_link': request.data['image_link'],
            'status': request.data['status'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Post " + old_name + " have been updated "
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = Post.objects.get(id=pk)
        objDestroy.delete()
        serializer = PostSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Post " + objDestroy.title + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data
