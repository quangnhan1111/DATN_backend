from brands.models import Brand
from brands.repository import BrandRepository


class BrandService:
    def __init__(self):
        self.brand_repository = BrandRepository()

    def get_list_no_paginate(self):
        brands = self.brand_repository.get_list_no_paginate()
        return brands

    def index(self):
        brands = self.brand_repository.index()
        return brands

    def store(self, request):
        data = self.brand_repository.store(request)
        return data

    def show(self, pk):
        if Brand.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Brand.objects.filter(deleted_at=False, id=pk).exists():
            return self.brand_repository.show(pk)
        return None

    def update(self, request, pk):
        if Brand.objects.filter(deleted_at=False, id=pk).exists():
            brandUpdate = Brand.objects.get(id=pk)
            return self.brand_repository.update(brandUpdate, request)
        return None

    def destroy(self, request, pk):
        if Brand.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Brand.objects.filter(deleted_at=False, id=pk).exists():
            return self.brand_repository.destroy(request, pk)
        return None

    def active(self, pk):
        if Brand.objects.filter(deleted_at=False, id=pk).exists():
            brandUpdate = Brand.objects.get(id=pk)
            return self.brand_repository.active(brandUpdate)
        return None
