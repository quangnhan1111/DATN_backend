from categories.models import Category
from categories.repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    def get_category_and_detail_subcategory(self):
        return self.category_repository.get_category_and_detail_subcategory()

    def get_list_no_paginate(self):
        categories = self.category_repository.get_list_no_paginate()
        return categories

    def index(self):
        categories = self.category_repository.index()
        return categories

    def store(self, request):
        data = self.category_repository.store(request)
        return data

    def show(self, pk):
        if Category.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Category.objects.filter(deleted_at=False, id=pk).exists():
            return self.category_repository.show(pk)
        return None

    def update(self, request, pk):
        # print(Category.objects.get(name='testCategory').id)
        if Category.objects.filter(deleted_at=False, id=pk).exists():
            categoryUpdate = Category.objects.get(id=pk)
            return self.category_repository.update(categoryUpdate, request)
        return None

    def destroy(self, request, pk):
        if Category.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Category.objects.filter(deleted_at=False, id=pk).exists():
            return self.category_repository.destroy(request, pk)
        return None

    def activate(self, pk):
        # print(Category.objects.get(name='testCategory').id)
        if Category.objects.filter(deleted_at=False, id=pk).exists():
            categoryUpdate = Category.objects.get(id=pk)
            return self.category_repository.activate(categoryUpdate)
        return None

