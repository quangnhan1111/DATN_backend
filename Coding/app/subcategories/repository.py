from django.contrib.auth.models import User

from .models import SubCategory
from .serializer import SubCategorySerializer
from notifications.models import Notifications


class SubCategoryRepository:
    def __init__(self):
        pass

    def activate(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = SubCategorySerializer(objUpdate)
        return serializer.data

    def get_sub_base_on_category(self, pk):
        subcategories = SubCategory.objects.filter(deleted_at=False, category_id=pk, category__deleted_at=False) \
            .values('name',
                    'category',
                    'category__name',
                    'status', 'id') \
            .order_by('-created_at')
        serializer = SubCategorySerializer(data=list(subcategories), many=True)
        serializer.is_valid(raise_exception=True)
        return subcategories

    def get_list_no_paginate(self):
        subcategories = SubCategory.objects.filter(deleted_at=False).order_by('-id').values('id', 'name',
                                                                                            'created_at',
                                                                                            'updated_at',
                                                                                            'category',
                                                                                            'category__name',
                                                                                            'status')
        serializer = SubCategorySerializer(data=list(subcategories), many=True)
        serializer.is_valid(raise_exception=True)
        return subcategories

    def index(self):
        subcategories = SubCategory.objects.filter(deleted_at=False).order_by('-id').values('id', 'name',
                                                                                            'created_at',
                                                                                            'updated_at',
                                                                                            'category',
                                                                                            'category__name',
                                                                                            'status')
        serializer = SubCategorySerializer(data=list(subcategories), many=True)
        serializer.is_valid(raise_exception=True)
        return [subcategories, subcategories.count()]

    def store(self, request):
        context = {'request': request}
        serializer = SubCategorySerializer(data={
            'name': request.data['name'],
            'category': request.data['category'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "SubCategory " + request.data['name'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        old_name = objUpdate.name
        serializer = SubCategorySerializer(instance=objUpdate, data={
            'name': request.data['name'],
            'category': request.data['category'],
            'status': request.data['status'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "SubCategory " + old_name + " have been updated to " + request.data['name']
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def show(self, pk):
        sub = SubCategory.objects.get(deleted_at=False, id=pk)
        serializer = SubCategorySerializer(sub, many=False)
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = SubCategory.objects.get(id=pk)
        objDestroy.delete()
        serializer = SubCategorySerializer(objDestroy, many=False)
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
