from django.contrib.auth.models import User

from .models import Coupon
from .serializer import CouponSerializer
from notifications.models import Notifications


class CouponRepository:
    def __init__(self):
        pass

    def activate(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = CouponSerializer(objUpdate)
        return serializer.data

    def get_list_no_paginate(self):
        coupons = Coupon.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'time', 'condition',
                                                                                 'value', 'name_code', 'status',
                                                                                 'created_at', 'updated_at')
        serializer = CouponSerializer(data=list(coupons), many=True)
        serializer.is_valid(raise_exception=True)
        return coupons

    def index(self):
        coupons = Coupon.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'time', 'condition',
                                                                                 'value', 'name_code', 'status',
                                                                                 'created_at', 'updated_at')
        serializer = CouponSerializer(data=list(coupons), many=True)
        serializer.is_valid(raise_exception=True)
        return [coupons, coupons.count()]

    def store(self, request):
        context = {'request': request}
        serializer = CouponSerializer(data={
            'name': request.data['name'],
            'time': request.data['time'],
            'condition': request.data['condition'],
            'value': request.data['value'],
            'name_code': request.data['name_code'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Coupon " + request.data['name'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        old_name = objUpdate.name
        serializer = CouponSerializer(instance=objUpdate, data={
            'name': request.data['name'],
            'time': request.data['time'],
            'condition': request.data['condition'],
            'value': request.data['value'],
            'name_code': request.data['name_code'],
            'status': request.data['status'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Coupon " + old_name + " have been updated to " + request.data['name']
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def show(self, pk):
        coupon = Coupon.objects.get(deleted_at=False, id=pk)
        serializer = CouponSerializer(coupon, many=False)
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = Coupon.objects.get(id=pk)
        objDestroy.delete()
        serializer = CouponSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Coupon " + objDestroy.name + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data
