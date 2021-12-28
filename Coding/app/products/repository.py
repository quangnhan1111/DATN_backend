from django.contrib.auth.models import User
from django.db.models import Sum, Avg, F

from notifications.models import Notifications
from .models import Product, Attribute, Attribute_Varchar, Attribute_Int, Attribute_Float, Product_Link, WishlistProduct
from .serializer import ProductSerializer


class ProductRepository:
    def __init__(self):
        pass

    def activate(self, objUpdate):
        status = False if objUpdate.status == True else True
        objUpdate.status = status
        objUpdate.save()
        serializer = ProductSerializer(objUpdate)
        return serializer.data

    def sorted_high_to_low(self):
        product_sorted_high_to_low = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False,
                    type='config', brand__deleted_at=False, ) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-price')

        list_res = list()
        for product in product_sorted_high_to_low:
            list_res.append(product)
        return list_res

    def sorted_low_to_high(self):
        product_sorted_high_to_low = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False,
                    type='config', brand__deleted_at=False, ) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('price')

        list_res = list()
        for product in product_sorted_high_to_low:
            list_res.append(product)
        return list_res

    def search_base_size(self, name_size):
        product_by_search = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False,
                    type='config', brand__deleted_at=False, ) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-created_at')

        list_res = list()
        # for product in product_by_search:
        #     if product['avgStar'] > int(rating):
        #         list_res.append(product)
        return list_res

    def search_base_review(self, rating):
        product_by_search = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False,
                    type='config', brand__deleted_at=False, ) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-created_at')

        list_res = list()
        for product in product_by_search:
            if product['avgStar'] is None:
                pass
            else:
                product['avgStar'] > float(rating)
                list_res.append(product)
        return list_res

    def search_base_price(self, price_min, price_max):
        product_by_search = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False,
                    type='config', brand__deleted_at=False, ) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-created_at')

        list_res = list()
        for product in product_by_search:
            if float(price_max) > product['price'] > float(price_min):
                list_res.append(product)
        return list_res

    def get_product_by_search(self, key):
        print(key)
        product_by_search = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False, subcategory__category__deleted_at=False,
                    type='config', brand__deleted_at=False, name__contains=key) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-created_at')

        return product_by_search

    def add_wishlist_product(self, request, idCustomer):
        product = WishlistProduct.objects.create(
            customer_id=int(idCustomer),
            product_id=request.data['product_id'],
        )
        product.save()
        print(product)
        return product

    def check_wishlist_product(selfS, idCustomer, idPro):
        if WishlistProduct.objects.filter(product_id=idPro, customer_id=idCustomer).exists():
            return 1
        return 0

    def get_wishlist_product(self, idCustomer):
        product_wishlist_by_customer = WishlistProduct.objects.filter(product__deleted_at=False,
                                                                      product__subcategory__deleted_at=False,
                                                                      product__subcategory__category__deleted_at=False,
                                                                      product__brand__deleted_at=False,
                                                                      customer_id=idCustomer) \
            .annotate(avgStar=Avg('product__review__star'),
                      Name_Brand=F('product__brand__name'),
                      Name_SubCategory=F('product__subcategory__name'),
                      Name_Category=F('product__subcategory__category__name'),
                      Name_Image=F('product__image_name'),
                      Link_Image=F('product__image_link'), ) \
            .values('product_id', 'product__name', 'product__des', 'product__gender', 'Name_Brand',
                    'Name_SubCategory', 'Name_Category', 'Name_Image',
                    'Link_Image', 'product__brand_id', 'product__subcategory__category_id',
                    'product__subcategory_id', 'product__created_at', 'avgStar') \
            .order_by('-product__created_at')

        return product_wishlist_by_customer

    def get_new_product(self):
        product_new = Product.objects \
                          .filter(deleted_at=False, subcategory__deleted_at=False,
                                  subcategory__category__deleted_at=False,
                                  type='config', brand__deleted_at=False) \
                          .annotate(avgStar=Avg('review__star'),
                                    Name_Brand=F('brand__name'),
                                    Name_SubCategory=F('subcategory__name'),
                                    Name_Category=F('subcategory__category__name'),
                                    Name_Image=F('image_name'),
                                    Link_Image=F('image_link'),
                                    number=Sum('product__product_link__attribute_int__value'),
                                    price=Avg('product__product_link__attribute_float__value'), ) \
                          .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                                  'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                                  'number', 'price', 'created_at', 'avgStar', 'status') \
                          .order_by('-created_at')[0:4]

        return product_new

    def get_best_product(self):
        product_best = Product.objects \
                           .filter(deleted_at=False, subcategory__deleted_at=False,
                                   subcategory__category__deleted_at=False,
                                   type='config', brand__deleted_at=False) \
                           .annotate(avgStar=Avg('review__star'),
                                     Name_Brand=F('brand__name'),
                                     Name_SubCategory=F('subcategory__name'),
                                     Name_Category=F('subcategory__category__name'),
                                     Name_Image=F('image_name'),
                                     Link_Image=F('image_link'),
                                     number=Sum('product__product_link__attribute_int__value'),
                                     price=Avg('product__product_link__attribute_float__value'),
                                     NumberSOLDOUT=F('invoicedetail__number'), ) \
                           .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                                   'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                                   'number', 'price', 'created_at', 'avgStar', 'NumberSOLDOUT', 'status') \
                           .order_by('-NumberSOLDOUT')[0:4]
        return product_best

    def get_related_product_by_brand(self, pk):
        product_related_product_by_brand = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False,
                    subcategory__category__deleted_at=False,
                    type='config', brand_id=pk) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-created_at')
        return product_related_product_by_brand

    def get_related_product_by_subcate(self, pk):
        product_related = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False,
                    subcategory__category__deleted_at=False,
                    type='config', subcategory_id=pk, brand__deleted_at=False) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-created_at')
        return product_related

    def get_related_product_by_cate(self, pk):
        product_related = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False,
                    subcategory__category__deleted_at=False,
                    type='config', subcategory__category_id=pk, brand__deleted_at=False) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'avgStar', 'status') \
            .order_by('-created_at')
        return product_related

    def index(self):
        product = Product.objects \
            .filter(deleted_at=False, subcategory__deleted_at=False,
                    subcategory__category__deleted_at=False,
                    type='config', brand__deleted_at=False) \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'),
                      number=Sum('product__product_link__attribute_int__value'),
                      price=Avg('product__product_link__attribute_float__value'), ) \
            .values('id', 'name', 'des', 'gender', 'Name_Brand', 'Name_SubCategory', 'Name_Category',
                    'image_name', 'image_link', 'brand_id', 'subcategory__category_id', 'subcategory_id',
                    'number', 'price', 'created_at', 'updated_at', 'avgStar', 'status') \
            .order_by('-created_at')

        return product

    def show(self, pk):
        product = Product.objects \
            .filter(deleted_at=False, brand__deleted_at=False, subcategory__deleted_at=False,
                    subcategory__category__deleted_at=False, id=pk, type='config') \
            .annotate(avgStar=Avg('review__star'),
                      Name_Brand=F('brand__name'),
                      Name_SubCategory=F('subcategory__name'),
                      Name_Category=F('subcategory__category__name'),
                      Name_Image=F('image_name'),
                      Link_Image=F('image_link'), ) \
            .values('id', 'name', 'des', 'Name_Brand', 'gender',
                    'Name_Category', 'image_name', 'image_link', 'brand_id', 'subcategory_id',
                    'subcategory__category_id', 'Name_SubCategory',
                    'created_at', 'avgStar', 'product__product_link',
                    'product__product_link__attribute_varchar__value',
                    'product__product_link__attribute_varchar__attribute_id',
                    'product__product_link__attribute_int__value',
                    'product__product_link__attribute_float__value', 'status') \
            .order_by('-created_at')
        data = []
        attribute_color_id = Attribute.objects.get(label='color').id
        attribute_size_id = Attribute.objects.get(label='size').id
        colors = []
        sizes = []
        product = list(product)
        for i in range(0, len(product)):
            product[i]['flag'] = 0

        for i in range(0, len(product)):
            if product[i]['flag'] != 1:
                if product[i]['product__product_link__attribute_varchar__attribute_id'] == attribute_color_id:
                    colors.append(product[i]['product__product_link__attribute_varchar__value'])
                if product[i]['product__product_link__attribute_varchar__attribute_id'] == attribute_size_id:
                    sizes.append(product[i]['product__product_link__attribute_varchar__value'])
                for j in range(i + 1, len(product)):
                    if product[i]['product__product_link'] == product[j]['product__product_link']:
                        if product[j]['product__product_link__attribute_varchar__attribute_id'] == attribute_color_id:
                            colors.append(product[j]['product__product_link__attribute_varchar__value'])
                            product[j]['flag'] = 1
                        if product[j]['product__product_link__attribute_varchar__attribute_id'] == attribute_size_id:
                            sizes.append(product[j]['product__product_link__attribute_varchar__value'])
                            product[j]['flag'] = 1
                data.append({
                    'id': product[0]['id'],
                    'name': product[0]['name'],
                    'des': product[0]['des'],
                    'Name_Brand': product[0]['Name_Brand'],
                    'gender': product[0]['gender'],
                    'Name_Category': product[0]['Name_Category'],
                    'Name_SubCategory': product[0]['Name_SubCategory'],
                    'Name_Image': product[0]['image_name'],
                    'Link_Image': product[0]['image_link'],
                    'brand_id': product[0]['brand_id'],
                    'subcategory_id': product[0]['subcategory_id'],
                    'subcategory__category_id': product[0]['subcategory__category_id'],
                    'created_at': product[0]['created_at'],
                    'avgStar': product[0]['avgStar'],
                    'status': product[0]['status'],
                    'price': product[i]['product__product_link__attribute_float__value'],
                    'number': product[i]['product__product_link__attribute_int__value'],
                    'colors': colors,
                    'sizes': sizes,
                    'product__product_link': product[i]['product__product_link'],
                })
            sizes = []
            colors = []
        return data

    def store(self, request):
        context = {'request': request}
        serializer = ProductSerializer(data={
            'name': request.data['name'],
            'des': request.data['des'],
            'subcategory': request.data['subcategory'],
            'brand': request.data['brand'],
            'gender': request.data['gender'],
            'image_name': request.data['image_name'],
            'image_link': request.data['image_link'],
            'type': 'config',
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notification
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Product " + request.data['name'] + " have been created"
            obj_notification.save()
            # end notification
        except:
            print("An exception occurred")
        return serializer.data

    def update(self, objUpdate, request):
        context = {'request': request}
        old_name = objUpdate.name
        serializer = ProductSerializer(instance=objUpdate, data={
            'name': request.data['name'],
            'des': request.data['des'],
            'subcategory': request.data['subcategory'],
            'brand': request.data['brand'],
            'gender': request.data['gender'],
            'image_name': request.data['image_name'],
            'image_link': request.data['image_link'],
            'type': request.data.get('type', 'None'),
            'status': request.data.get('status', 'None'),
        }, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Product " + old_name + " have been updated "
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data

    def destroy(self, request, pk):
        objDestroy = Product.objects.get(id=pk)
        products = Product.objects.filter(name=objDestroy.name, type='simple')
        for product in products:
            Attribute_Varchar.objects.filter(product_id=product.id).delete()
            Attribute_Int.objects.filter(product_id=product.id).delete()
            Attribute_Float.objects.filter(product_id=product.id).delete()
        Product_Link.objects.filter(product_id=objDestroy.id).delete()
        products.delete()
        Product.objects.filter(id=pk).delete()
        serializer = ProductSerializer(objDestroy, many=False)
        try:
            # notifications
            user = User.objects.get(id=request.user.id)
            obj_notification = Notifications()
            obj_notification.created_by = user
            obj_notification.notification = "Product " + objDestroy.name + " have been deleted"
            obj_notification.save()
            # end
        except:
            print("An exception occurred")
        return serializer.data
