from colors.models import Color
from colors.repository import ColorRepository


class ColorService():
    def __init__(self):
        self.color_repository = ColorRepository()

    def get_list_no_paginate(self):
        colors = self.color_repository.get_list_no_paginate()
        return colors

    def get_color_by_product(self, product_id):
        colors = self.color_repository.get_color_by_product(product_id)
        return colors

    def get_size_by_product(self, product_id):
        colors = self.color_repository.get_size_by_product(product_id)
        return colors

    def index(self):
        colors = self.color_repository.index()
        return colors

    def store(self, request):
        data = self.color_repository.store(request)
        return data

    def show(self, pk):
        if Color.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Color.objects.filter(deleted_at=False, id=pk).exists():
            return self.color_repository.show(pk)
        return None

    def update(self, request, pk):
        if Color.objects.filter(deleted_at=False, id=pk).exists():
            colorUpdate = Color.objects.get(id=pk)
            return self.color_repository.update(colorUpdate, request)
        return None

    def destroy(self, request, pk):
        if Color.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Color.objects.filter(deleted_at=False, id=pk).exists():
            return self.color_repository.destroy(request, pk)
        return None

    def active(self, pk):
        if Color.objects.filter(deleted_at=False, id=pk).exists():
            colorUpdate = Color.objects.get(id=pk)
            return self.color_repository.active(colorUpdate)
        return None

