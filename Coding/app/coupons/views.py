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
from .models import Coupon
from .serializer import CouponSerializer
from .service import CouponService


@api_view(['GET'])
def get_list_no_paginate(request):
    coupon_service = CouponService()
    coupons = coupon_service.get_list_no_paginate()
    content = response(coupons, 'successfully', True)
    return Response(data=content, status=status.HTTP_200_OK)


class CouponView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.coupon_service = CouponService()

    def get(self, request):
        # print(available_perm_status(request.user))
        current_page = int(request.GET.get('page', 1))
        [start, end, per_page] = paginate(current_page)
        user = request.user
        if has_permission(user, 'view_coupon'):
            [coupons, count] = self.coupon_service.index()
            content = response(coupons[start:end], 'successfully', True, count, current_page,
                               math.ceil(count / per_page), per_page)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        user = request.user
        if has_permission(user, 'add_coupon'):
            if Coupon.objects.filter(deleted_at=False, name=request.data['name']).first():
                return Response('name Coupon is taken.')
            if Coupon.objects.filter(deleted_at=True, name=request.data['name']).first():
                objRestore = Coupon.objects.get(name=request.data['name'])
                objRestore.restore()
                serializer = CouponSerializer(objRestore)
                content = response(serializer.data, 'successfully', True)
                return Response(data=content, status=status.HTTP_200_OK)
            coupon = self.coupon_service.store(request)
            content = response(coupon, 'successfully', True)
            return Response(data=content, status=status.HTTP_201_CREATED)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'change_coupon'):
            coupon = self.coupon_service.update(request, pk)
            if coupon is None:
                content = response(None, 'None Object exist', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(coupon, 'successfully', True)
            return Response(data=content, status=status.HTTP_206_PARTIAL_CONTENT)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        user = request.user
        pk = request.query_params["id"]
        if has_permission(user, 'delete_coupon'):
            coupon = self.coupon_service.destroy(request, pk)
            if coupon is None:
                content = response(None, 'None Object', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            if coupon == 'obj destroyed':
                content = response(None, 'Object Destroyed', True)
                return Response(data=content, status=status.HTTP_204_NO_CONTENT)
            content = response(coupon, 'successfully', True)
            return Response(data=content, status=status.HTTP_200_OK)
        content = response('Forbidden', 'failure', False)
        return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_details(request, pk):
    coupon_service = CouponService()
    user = request.user
    if has_permission(user, 'view_coupon'):
        coupon = coupon_service.show(pk)
        if coupon is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if coupon == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(coupon, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def activate(request, pk):
    coupon_service = CouponService()
    user = request.user
    if has_permission(user, 'change_coupon'):
        coupon = coupon_service.activate(pk)
        if coupon is None:
            content = response(None, 'None Object', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        if coupon == 'obj destroyed':
            content = response(None, 'Object Destroyed', True)
            return Response(data=content, status=status.HTTP_204_NO_CONTENT)
        content = response(coupon, 'successfully', True)
        return Response(data=content, status=status.HTTP_200_OK)
    content = response('Forbidden', 'failure', False)
    return Response(data=content, status=status.HTTP_403_FORBIDDEN)
