import math

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import available_perm_status

from app.utils import paginate, response
from posts.models import Post
from posts.serializer import PostSerializer
from posts.service import PostService


@api_view(['GET'])
def get_list(request):
    post_service = PostService()
    current_page = int(request.GET.get('page', 1))
    [start, end, per_page] = paginate(current_page)
    [posts, count] = post_service.index()
    content = response(posts[start:end], 'successfully', True, count, current_page,
                       math.ceil(count / per_page), per_page)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_list_no_page(request):
    post_service = PostService()
    posts = post_service.get_list_no_page()
    content = response(posts, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


class PostView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.post_service = PostService()

    def get(self, request):
        user = request.user
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        if has_permission(user, 'view_post'):
            [posts, count] = self.post_service.index()
            content = response(posts[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_post'):
            if Post.objects.filter(deleted_at=False, title=request.data['title']).first():
                return Response('title Post is taken.')
            if Post.objects.filter(deleted_at=True, title=request.data['title']).first():
                objRestore = Post.objects.get(title=request.data['title'])
                objRestore.restore()
                serializer = PostSerializer(objRestore)
                content = response(serializer.data, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            post = self.post_service.store(request)
            content = response(post, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_post'):
            post = self.post_service.update(request, pk)
            if post is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(post, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_post'):
            post = self.post_service.destroy(request, pk)
            if post is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if post == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(post, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_details(request, pk):
    post_service = PostService()
    post = post_service.show(pk)
    if post is None:
        content = response(None, 'None Object', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    if post == 'obj destroyed':
        content = response(None, 'Object Destroyed', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    content = response(post, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activate(request, pk):
    user = request.user
    post_service = PostService()
    post = post_service.activate(pk)
    print(request.user)
    if has_permission(user, 'change_post'):
        if post is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if post == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(post, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)
