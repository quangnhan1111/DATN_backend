from categories.models import Category
from .models import SubCategory
from .repository import SubCategoryRepository


class SubCategoryService:
    def __init__(self):
        self.subcategory_repository = SubCategoryRepository()

    def get_sub_base_on_category(self, pk):
        if Category.objects.filter(deleted_at=False, id=pk).exists():
            subcategories = self.subcategory_repository.get_sub_base_on_category(pk)
            return subcategories
        return None

    def activate(self, pk):
        # print(SubCategory.objects.all())
        if SubCategory.objects.filter(deleted_at=False, id=pk).exists():
            categoryUpdate = SubCategory.objects.get(id=pk)
            return self.subcategory_repository.activate(categoryUpdate)
        return None

    def get_list_no_paginate(self):
        subcategories = self.subcategory_repository.get_list_no_paginate()
        return subcategories

    def index(self):
        subcategories = self.subcategory_repository.index()
        return subcategories

    def store(self, request):
        data = self.subcategory_repository.store(request)
        return data

    def show(self, pk):
        if SubCategory.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if SubCategory.objects.filter(deleted_at=False, id=pk).exists():
            return self.subcategory_repository.show(pk)
        return None

    def update(self, request, pk):
        print(SubCategory.objects.all())
        if SubCategory.objects.filter(deleted_at=False, id=pk).exists():
            categoryUpdate = SubCategory.objects.get(id=pk)
            return self.subcategory_repository.update(categoryUpdate, request)
        return None

    def destroy(self, request, pk):
        print(SubCategory.objects.all())
        if SubCategory.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if SubCategory.objects.filter(deleted_at=False, id=pk).exists():
            return self.subcategory_repository.destroy(request, pk)
        return None

