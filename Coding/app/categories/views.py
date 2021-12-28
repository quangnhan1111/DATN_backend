# Create your views here.
import math

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission

from app.utils import response, paginate
from categories.models import Category
from categories.serializer import CategorySerializer
from categories.service import CategoryService


@api_view(['GET'])
def get_list_no_paginate(request):
    category_service = CategoryService()
    categories = category_service.get_list_no_paginate()
    content = response(categories, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


class CategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.category_service = CategoryService()

    def get(self, request):
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        user = request.user
        if has_permission(user, 'view_category'):
            [categories, count] = self.category_service.index()
            content = response(categories[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_category'):
            if Category.objects.filter(deleted_at=False, name=request.data['name']).first():
                return Response('name Category is taken.')
            if Category.objects.filter(deleted_at=True, name=request.data['name']).first():
                objRestore = Category.objects.get(name=request.data['name'])
                objRestore.restore()
                serializer = CategorySerializer(objRestore)
                content = response(serializer.data, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            category = self.category_service.store(request)
            content = response(category, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_category'):
            category = self.category_service.update(request, pk)
            if category is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(category, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_category'):
            category = self.category_service.destroy(request, pk)
            if category is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if category == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(category, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_details(request, pk):
    category_service = CategoryService()
    user = request.user
    if has_permission(user, 'view_category'):
        category = category_service.show(pk)
        if category is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if category == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(category, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_category_and_detail_subcategory(request):
    category_service = CategoryService()
    category = category_service.get_category_and_detail_subcategory()
    content = response(category, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activate(request, pk):
    category_service = CategoryService()
    user = request.user
    if has_permission(user, 'change_category'):
        category = category_service.activate(pk)
        if category is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if category == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(category, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)

