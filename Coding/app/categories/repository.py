from django.contrib.auth.models import User

from notifications.models import Notifications
from .models import Category
from .serializer import CategorySerializer, CategoryDetailSerializer


class CategoryRepository:
    def __init__(self):
        pass

    def activate(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = CategorySerializer(objUpdate)
        return serializer.data

    def get_list_no_paginate(self):
        categories = Category.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'created_at',
                                                                                      'updated_at', 'status')
        serializer = CategorySerializer(data=list(categories), many=True)
        serializer.is_valid(raise_exception=True)
        return categories

    def index(self):
        categories = Category.objects.filter(deleted_at=False).order_by('-id').values('id', 'name', 'created_at',
                                                                                      'updated_at', 'status')
        serializer = CategorySerializer(data=list(categories), many=True)
        serializer.is_valid(raise_exception=True)
        return [categories, categories.count()]

    def store(self, request):
        context = {'request': request}
        serializer = CategorySerializer(data={
            'name': request.data['name'],
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Category " + request.data['name'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        old_name = objUpdate.name
        serializer = CategorySerializer(instance=objUpdate, data={
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
            obj_notification.notification = "Category " + old_name + " have been updated to " + request.data['name']
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def add_sub_into_cate(self, list_category, sub_list, item):
        sub_list.append({
            'id': item['subcategory'],
            'name': item['subcategory__name']
        })
        list_category.append({
            'id': item['id'],
            'name': item['name'],
            'children': sub_list
        })

    def get_category_and_detail_subcategory(self):
        category = Category.objects.filter(deleted_at=False).exclude(subcategory=None).values('id', 'name',
                                                                                              'status',
                                                                                              'created_at',
                                                                                              'updated_at',
                                                                                              'subcategory__name',
                                                                                              'subcategory')
        list_category = []
        for item in category:
            if list_category:
                flag = 0
                for index in list_category:
                    if index['id'] == item['id']:
                        flag = 1
                        index['children'].append({
                            'id': item['subcategory'],
                            'name': item['subcategory__name']
                        })
                        break
                if flag == 0:
                    sub_list = list()
                    self.add_sub_into_cate(list_category, sub_list, item)
            else:
                sub_list = list()
                self.add_sub_into_cate(list_category, sub_list, item)
        print(list_category)
        serializer = CategoryDetailSerializer(instance=list_category, many=True)
        return serializer.data

    def show(self, pk):
        category = Category.objects.filter(deleted_at=False, id=pk).get()
        serializer = CategorySerializer(category, many=False)
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = Category.objects.get(id=pk)
        objDestroy.delete()
        serializer = CategorySerializer(objDestroy, many=False)
        # serializer.is_valid(raise_exception=True)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Category " + objDestroy.name + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data
