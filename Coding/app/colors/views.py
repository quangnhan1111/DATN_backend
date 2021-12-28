# Create your views here.
# Create your views here.
import math

from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission
from app.utils import response, paginate
from colors.models import Color
from colors.serializer import ColorSerializer
from colors.service import ColorService


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_list_no_paginate(request):
    color_service = ColorService()
    user = request.user
    if has_permission(user, 'view_color'):
        # if True:
        colors = color_service.get_list_no_paginate()
        content = response(colors, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_color_by_product(request, product_id):
    color_service = ColorService()
    colors = color_service.get_color_by_product(product_id)
    content = response(colors, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_size_by_product(request, product_id):
    color_service = ColorService()
    user = request.user
    # print(available_perm_status(request.user))
    colors = color_service.get_size_by_product(product_id)
    content = response(colors, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


class ColorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.color_service = ColorService()

    def get(self, request):
        user = request.user
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        if has_permission(user, 'view_color'):
            [colors, count] = self.color_service.index()
            content = response(colors[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_color'):
            if Color.objects.filter(deleted_at=False, name=request.data['name']).first():
                return Response('name Color is taken.')
            if Color.objects.filter(deleted_at=True, name=request.data['name']).first():
                objRestore = Color.objects.get(name=request.data['name'])
                objRestore.restore()
                serializer = ColorSerializer(objRestore)
                content = response(serializer.data, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            color = self.color_service.store(request)
            content = response(color, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_color'):
            color = self.color_service.update(request, pk)
            if color is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(color, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_color'):
            color = self.color_service.destroy(request, pk)
            if color is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if color == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(color, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_details(request, pk):
    color_service = ColorService()
    user = request.user
    if has_permission(user, 'view_color'):
        color = color_service.show(pk)
        if color is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if color == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(color, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_protect
def active(request, pk):
    color_service = ColorService()
    user = request.user
    if has_permission(user, 'change_color'):
        color = color_service.active(pk)
        if color is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if color == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(color, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)
