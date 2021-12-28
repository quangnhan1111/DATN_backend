from django.contrib.auth.models import User
from notifications.models import Notifications
from products.models import Product
from .models import Color
from .serializer import ColorSerializer


class ColorRepository:
    def __init__(self):
        pass

    def get_color_by_product(self, product_id):
        # product = Product.objects.filter(deleted_at=False,
        #                                  subcategory__deleted_at=False,
        #                                  brand__deleted_at=False) \
        #     .filter(id=product_id).values('colors__name', 'colors')
        # return product
        pass

    def get_size_by_product(self, product_id):
        # product = Product.objects.filter(deleted_at=False, genders__deleted_at=False,
        #                                  categories__deleted_at=False, brands__deleted_at=False) \
        #     .filter(id=product_id).values('size', 'size__name')
        # return product

        pass

    def get_list_no_paginate(self):
        colors = Color.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'created_at',
                                                                               'updated_at', 'status')
        serializer = ColorSerializer(data=list(colors), many=True)
        serializer.is_valid(raise_exception=True)
        return colors

    def index(self):
        colors = Color.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'created_at',
                                                                               'updated_at', 'status')
        serializer = ColorSerializer(data=list(colors), many=True)
        serializer.is_valid(raise_exception=True)
        return [colors, colors.count()]

    def store(self, request):
        context = {'request': request}
        serializer = ColorSerializer(data={
            'name': request.data['name'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Color " + request.data['name'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        old_name = objUpdate.name
        serializer = ColorSerializer(instance=objUpdate, data={
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
            obj_notification.notification = "Color " + old_name + " have been updated to " + request.data['name']
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def show(self, pk):
        color = Color.objects.filter(deleted_at=False, id=pk).get()
        serializer = ColorSerializer(color, many=False)
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = Color.objects.get(id=pk)
        objDestroy.delete()
        serializer = ColorSerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Color " + objDestroy.name + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def active(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = ColorSerializer(objUpdate)
        return serializer.data
