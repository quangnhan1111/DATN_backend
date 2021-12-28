
import math

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.checkers import has_permission

from app.utils import response, paginate
from .models import SubCategory
from .serializer import SubCategorySerializer
from .service import SubCategoryService


@api_view(['GET'])
def get_list_no_paginate(request):
    subcategory_service = SubCategoryService()
    subcategories = subcategory_service.get_list_no_paginate()
    content = response(subcategories, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


class SubCategoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.subcategory_service = SubCategoryService()

    def get(self, request):
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        user = request.user
        if has_permission(user, 'view_subcategory'):
            [subcategories, count] = self.subcategory_service.index()
            content = response(subcategories[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_subcategory'):
            if SubCategory.objects.filter(deleted_at=False, name=request.data['name']).first():
                return Response('name SubCategory is taken.')
            if SubCategory.objects.filter(deleted_at=True, name=request.data['name']).first():
                objRestore = SubCategory.objects.get(name=request.data['name'])
                objRestore.restore()
                serializer = SubCategorySerializer(objRestore)
                content = response(serializer.data, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            subcategories = self.subcategory_service.store(request)
            content = response(subcategories, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_subcategory'):
            subcategories = self.subcategory_service.update(request, pk)
            if subcategories is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(subcategories, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_subcategory'):
            subcategories = self.subcategory_service.destroy(request, pk)
            if subcategories is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if subcategories == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(subcategories, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_details(request, pk):
    subcategory_service = SubCategoryService()
    user = request.user
    if has_permission(user, 'view_subcategory'):
        subcategory = subcategory_service.show(pk)
        if subcategory is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if subcategory == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(subcategory, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activate(request, pk):
    subcategory_service = SubCategoryService()
    user = request.user
    if has_permission(user, 'change_subcategory'):
        subcategory = subcategory_service.activate(pk)
        if subcategory is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if subcategory == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(subcategory, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_sub_base_on_category(request, pk):
    subcategory_service = SubCategoryService()
    user = request.user
    subcategory = subcategory_service.get_sub_base_on_category(pk)
    if subcategory is None:
        content = response(None, 'None Object', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    if subcategory == 'obj destroyed':
        content = response(None, 'Object Destroyed', True)
        return Response(data=content, status=status.HTTP_204_NO_CONTENT)
    content = response(subcategory, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)