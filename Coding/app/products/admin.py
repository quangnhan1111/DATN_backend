from django.contrib import admin

# Register your models here.
from products.models import Product, Attribute_Float, Attribute_Varchar, Attribute, Product_Link, Attribute_Int, \
    WishlistProduct

admin.site.register(Product)
admin.site.register(Product_Link)
admin.site.register(Attribute)
admin.site.register(Attribute_Varchar)
admin.site.register(Attribute_Float)
admin.site.register(Attribute_Int)
admin.site.register(WishlistProduct)