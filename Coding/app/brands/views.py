import math

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import available_perm_status

from app.utils import paginate, response
from brands.models import Brand
from brands.serializer import BrandSerializer
from brands.service import BrandService


@api_view(['GET'])
def get_list_no_paginate(request):
    brand_service = BrandService()
    brands = brand_service.get_list_no_paginate()
    content = response(brands, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


class BrandView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.brand_service = BrandService()

    def get(self, request):
        print(available_perm_status(request.user))
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        user = request.user
        if has_permission(user, 'view_brand'):
            [brands, count] = self.brand_service.index()
            content = response(brands[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_brand'):
            if Brand.objects.filter(deleted_at=False, name=request.data['name']).first():
                return Response('name Brand is taken.')
            if Brand.objects.filter(deleted_at=True, name=request.data['name']).first():
                objRestore = Brand.objects.get(name=request.data['name'])
                objRestore.restore()
                serializer = BrandSerializer(objRestore)
                content = response(serializer.data, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            brand = self.brand_service.store(request)
            content = response(brand, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_brand'):
            brand = self.brand_service.update(request, pk)
            if brand is None:
                content = response(None, 'None Object exist', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(brand, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_brand'):
            brand = self.brand_service.destroy(request, pk)
            if brand is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if brand == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(brand, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_details(request, pk):
    brand_service = BrandService()
    user = request.user
    if has_permission(user, 'view_brand'):
        brand = brand_service.show(pk)
        if brand is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if brand == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(brand, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activate(request, pk):
    brand_service = BrandService()
    user = request.user
    if has_permission(user, 'change_brand'):
        brand = brand_service.active(pk)
        if brand is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if brand == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(brand, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)
