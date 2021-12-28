from products.models import Product
from products.repository import ProductRepository


class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def sorted_high_to_low(self):
        products = self.product_repository.sorted_high_to_low()
        return products

    def sorted_low_to_high(self):
        products = self.product_repository.sorted_low_to_high()
        return products

    def search_base_price(self, price_min, price_max):
        products = self.product_repository.search_base_price(price_min, price_max)
        return products

    def search_base_review(self, rating):
        products = self.product_repository.search_base_review(rating)
        return products

    def search_base_size(self, name_size):
        products = self.product_repository.search_base_size(name_size)
        return products

    def check_wishlist_product(self, idCustomer, idPro):
        check = self.product_repository.check_wishlist_product(idCustomer, idPro)
        return check

    def get_wishlist_product(self, idCustomer):
        products = self.product_repository.get_wishlist_product(idCustomer)
        return products

    def add_wishlist_product(self, request, idCustomer):
        data = self.product_repository.add_wishlist_product(request, idCustomer)
        return data

    def get_product_by_search(self, key):
        products = self.product_repository.get_product_by_search(key)
        return products

    def get_new_product(self):
        products = self.product_repository.get_new_product()
        return products

    def get_best_product(self):
        products = self.product_repository.get_best_product()
        return products

    def get_related_product_by_brand(self, pk):
        products = self.product_repository.get_related_product_by_brand(pk)
        return products

    def get_related_product_by_subcate(self, pk):
        products = self.product_repository.get_related_product_by_subcate(pk)
        return products

    def get_related_product_by_cate(self, pk):
        products = self.product_repository.get_related_product_by_cate(pk)
        return products

    def index(self):
        products = self.product_repository.index()
        return products

    def store(self, request):
        data = self.product_repository.store(request)
        return data

    def show(self, pk):
        if Product.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Product.objects.filter(deleted_at=False, id=pk).exists():
            return self.product_repository.show(pk)
        return None

    def update(self, request, pk):
        if Product.objects.filter(deleted_at=False, id=pk).exists():
            objUpdate = Product.objects.get(id=pk)
            return self.product_repository.update(objUpdate, request)
        return None

    def destroy(self, request, pk):
        if Product.objects.filter(deleted_at=True, id=pk).exists():
            return 'obj destroyed'
        if Product.objects.filter(deleted_at=False, id=pk).exists():
            return self.product_repository.destroy(request, pk)
        return None

    def activate(self, pk):
        if Product.objects.filter(deleted_at=False, id=pk).exists():
            objUpdate = Product.objects.get(id=pk)
            return self.product_repository.activate(objUpdate)
        return None
