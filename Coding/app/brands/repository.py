from django.contrib.auth.models import User

from brands.models import Brand
from brands.serializer import BrandSerializer
from notifications.models import Notifications


class BrandRepository:
    def __init__(self):
        pass

    def active(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = BrandSerializer(objUpdate)
        return serializer.data

    def get_list_no_paginate(self):
        brands = Brand.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'created_at',
                                                                               'updated_at', 'status')
        serializer = BrandSerializer(data=list(brands), many=True)
        serializer.is_valid(raise_exception=True)
        return brands

    def index(self):
        brands = Brand.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'created_at',
                                                                               'updated_at', 'status')
        serializer = BrandSerializer(data=list(brands), many=True)
        serializer.is_valid(raise_exception=True)
        return [brands, brands.count()]

    def store(self, request):
        context = {'request': request}
        serializer = BrandSerializer(data={
            'name': request.data['name'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Brand " + request.data['name'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        print(request.data)
        context = {'request': request}
        old_name = objUpdate.name
        serializer = BrandSerializer(instance=objUpdate, data={
            'name': request.data['name'],
            'status': request.data['status'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Brand " + old_name + " have been updated to " + request.data['name']
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def show(self, pk):
        brand = Brand.objects.get(deleted_at=False, id=pk)
        serializer = BrandSerializer(brand, many=False)
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = Brand.objects.get(id=pk)
        objDestroy.delete()
        serializer = BrandSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Brand " + objDestroy.name + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data
