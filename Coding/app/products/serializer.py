from django.db.models import Q
from rest_framework import serializers
from products.models import Product, Product_Link, Attribute_Varchar, Attribute, Attribute_Float, Attribute_Int


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        # self.context['request'].data['roles']
        request = self.context['request']
        product_config = Product.objects.create(
            name=request.data['name'],
            des=request.data['des'],
            subcategory_id=request.data['subcategory'],
            brand_id=request.data['brand'],
            gender=request.data['gender'],
            image_name=request.data['image_name'],
            image_link=request.data['image_link'],
            type='config'
        )
        # product_config.save()
        self.save_product(request, product_config)
        return product_config

    def update(self, instance, validated_data):
        request = self.context['request']
        products = Product.objects.filter(name=instance.name, type='simple')
        instance.name = validated_data.get('name', instance.name)
        instance.des = validated_data.get('des', instance.des)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.image_name = validated_data.get('image_name', instance.image_name)
        instance.image_link = validated_data.get('image_link', instance.image_link)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        # xoa cac moi quan he
        for product in products:
            Attribute_Varchar.objects.filter(product_id=product.id).delete()
            Attribute_Int.objects.filter(product_id=product.id).delete()
            Attribute_Float.objects.filter(product_id=product.id).delete()
        Product_Link.objects.filter(product_id=instance.id).delete()
        products.delete()
        # end
        self.save_product(request, instance)
        return instance

    def save_product(self, request, product_config):
        list_item = request.data['list_item']
        print(Attribute.objects.get(label='color'))
        attribute_color_id = Attribute.objects.get(label='color').id
        attribute_size_id = Attribute.objects.get(label='size').id
        attribute_price_id = Attribute.objects.get(label='price').id
        attribute_number_id = Attribute.objects.get(label='number').id
        for item in list_item:
            product = Product.objects.create(
                name=request.data['name'],
                des=request.data['des'],
                subcategory_id=request.data['subcategory'],
                brand_id=request.data['subcategory'],
                gender=request.data['gender'],
                image_name=request.data['image_name'],
                image_link=request.data['image_link'],
                type='simple'
            )
            product.save()
            connect_product = Product_Link.objects.create(product_id=product_config.id, product_link_id=product.id)
            connect_product.save()
            save_color = Attribute_Varchar.objects.create(attribute_id=attribute_color_id, product_id=product.id,
                                                          value=item['color'])
            save_color.save()
            save_size = Attribute_Varchar.objects.create(attribute_id=attribute_size_id, product_id=product.id,
                                                         value=item['size'])
            save_size.save()
            save_price = Attribute_Float.objects.create(attribute_id=attribute_price_id, product_id=product.id,
                                                        value=item['price'])
            save_price.save()
            save_number = Attribute_Int.objects.create(attribute_id=attribute_number_id, product_id=product.id,
                                                       value=item['number'])
            save_number.save()
